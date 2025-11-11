"""
In this file, I define my LiveKit conversational voice agent.
I’ve built it so it can talk naturally, listen actively, and decide
intelligently when to pause or continue based on user intent.
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    AgentStateChangedEvent,
)
from livekit.plugins import silero, openai, deepgram, cartesia
from livekit import rtc

from interruption_handler import InterruptionHandler, InterruptionConfig

# I like to keep logging simple and informative.
log = logging.getLogger("conversational-agent")
logging.basicConfig(level=logging.INFO)

# I make sure my environment variables are available everywhere.
load_dotenv()


class ConversationalAgent(Agent):
    """
    This is my main conversational agent. It inherits from LiveKit’s base Agent
    class and uses my custom interruption handler to manage user interruptions
    more naturally.
    """

    def __init__(self, speech_filter: InterruptionHandler):
        """
        When I create my agent, I store a reference to my speech filter
        so I can check user transcripts on the fly.
        """
        super().__init__(
            instructions=(
                "You are a friendly and thoughtful voice assistant. "
                "Respond clearly, keep replies short, and sound natural."
            )
        )
        self.filter = speech_filter
        self._currently_speaking = False
        self.session_ref = None

    async def on_enter(self):
        """
        This method is called when I first join a LiveKit session.
        I usually greet the user here to start the conversation naturally.
        """
        log.info("I have entered the session successfully.")
        await self.session.generate_reply(
            instructions="Hi there! How can I assist you today?"
        )

    async def on_exit(self):
        """When I leave the session, I log that I’ve exited cleanly."""
        log.info("I have exited the session.")


def warmup_models(proc: JobProcess):
    """
    Before handling live audio, I pre-load all the heavy models
    (like the Voice Activity Detector) so I can start faster.
    """
    log.info("I’m preloading my Silero VAD model for efficiency...")
    proc.userdata["vad"] = silero.VAD.load()
    log.info("VAD model ready.")


async def run_agent(ctx: JobContext):
    """
    This is my main entrypoint.
    Here I set up my LiveKit session, initialize the models,
    and connect all the event listeners for speech and state updates.
    """

    # Attach useful context info for debugging.
    ctx.log_context_fields = {"room": ctx.room.name}
    log.info(f"Starting agent in room: {ctx.room.name}")

    # Load ignored words and thresholds from environment
    ignored_raw = os.getenv("IGNORED_WORDS", "uh,umm,hmm,haan,um,er,ah")
    ignored_words = [w.strip() for w in ignored_raw.split(",") if w.strip()]
    conf_threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))

    # Build my speech filter configuration
    config = InterruptionConfig.from_word_list(
        words=ignored_words,
        confidence_limit=conf_threshold,
        allow_dynamic_updates=True
    )

    # Create my speech filter
    speech_filter = InterruptionHandler(config)
    log.info(f"My speech filter is active with {len(ignored_words)} ignored words.")

    # Create the agent itself
    agent = ConversationalAgent(speech_filter)

    # Connect to the LiveKit room
    await ctx.connect()

    # Define my agent session with STT, LLM, and TTS pipeline
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(model="nova-3"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(),
        resume_false_interruption=True,
        false_interruption_timeout=1.5,
        min_interruption_duration=0.3,
        min_interruption_words=0,
    )

    agent.session_ref = session

    # Track when the agent starts or stops speaking
    @session.on("agent_state_changed")
    def on_agent_state_change(ev: AgentStateChangedEvent):
        prev_state = agent._currently_speaking
        agent._currently_speaking = ev.new_state == "speaking"

        if not prev_state and agent._currently_speaking:
            log.info("I just started speaking.")
        elif prev_state and not agent._currently_speaking:
            log.info(f"I stopped speaking; now I’m in '{ev.new_state}' state.")

    # Keep a buffer for timing analysis (optional future metrics)
    vad_start_time = None

    @session.on("user_started_speaking")
    def when_user_starts(ev):
        """
        Whenever the user starts talking, I mark the timestamp
        so I can measure how long they spoke.
        """
        nonlocal vad_start_time
        vad_start_time = asyncio.get_event_loop().time()
        if agent._currently_speaking:
            log.debug("User began speaking while I was still talking.")

    @session.on("user_stopped_speaking")
    def when_user_stops(ev):
        """
        When the user stops speaking, I calculate how long
        the utterance lasted — helpful for analytics.
        """
        nonlocal vad_start_time
        if vad_start_time:
            duration = asyncio.get_event_loop().time() - vad_start_time
            vad_start_time = None
            log.debug(f"User speech lasted for {duration:.2f} seconds.")

    @session.on("user_transcript")
    def handle_user_transcript(ev):
        """
        Every time the ASR generates a transcript, I analyze it
        to decide whether it’s a real interruption or just filler.
        """
        text = getattr(ev, "text", "")
        conf = getattr(ev, "confidence", None)
        is_final = getattr(ev, "is_final", False)

        if not text:
            return

        log.debug(f"Transcript ({'final' if is_final else 'interim'}): '{text}' ({conf})")

        # I only act on final transcripts when I’m currently speaking.
        if agent._currently_speaking and is_final:
            ignore_it = speech_filter.should_ignore_speech(text, conf)

            if ignore_it:
                log.info(f"🔇 I ignored a filler input: '{text}' (conf: {conf})")
                # I keep speaking normally.
                return
            else:
                log.info(f"✅ I detected a valid interruption: '{text}'")
                # LiveKit handles the stop automatically when true interruption is found.

    # Finally, I start the session and let everything run asynchronously.
    await session.start(agent=agent, room=ctx.room)
    log.info("Agent session fully initialized and running.")


# I register my entrypoint and prewarm functions with the CLI runner.
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=run_agent, prewarm_fnc=warmup_models))
