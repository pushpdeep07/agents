"""
In this file, I handle all the configuration for my LiveKit voice agent.
I load everything from environment variables so that my setup stays flexible
and easy to modify without touching the code.
"""

import os
from dataclasses import dataclass
from typing import List


@dataclass
class AgentConfig:
    """
    I use this dataclass to hold every important setting that my agent
    and speech filter depend on. It keeps things clean and strongly typed.
    """

    # LiveKit connection parameters
    livekit_url: str
    livekit_api_key: str
    livekit_api_secret: str

    # Interruption handling parameters
    ignored_words: List[str]
    confidence_limit: float
    allow_dynamic_updates: bool

    # Behavioral tuning parameters
    min_interrupt_time: float
    false_interrupt_delay: float
    resume_on_false: bool

    @classmethod
    def from_env(cls) -> 'AgentConfig':
        """
        Here I load all the environment variables that control my agent.
        If some variables aren’t provided, I fall back to safe defaults.
        """
        # LiveKit parameters
        url = os.getenv("LIVEKIT_URL", "wss://localhost:7880")
        key = os.getenv("LIVEKIT_API_KEY", "")
        secret = os.getenv("LIVEKIT_API_SECRET", "")

        # Filler and confidence handling
        fillers = os.getenv("IGNORED_WORDS", "uh,umm,hmm,haan,um,er,ah")
        ignored_list = [w.strip() for w in fillers.split(",") if w.strip()]

        conf_limit = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
        dynamic_update = os.getenv("ENABLE_DYNAMIC_UPDATES", "false").lower() == "true"

        # Timing and resumption settings
        min_interrupt = float(os.getenv("MIN_INTERRUPTION_DURATION", "0.3"))
        false_delay = float(os.getenv("FALSE_INTERRUPTION_TIMEOUT", "1.5"))
        resume_false = os.getenv("RESUME_FALSE_INTERRUPTION", "true").lower() == "true"

        return cls(
            livekit_url=url,
            livekit_api_key=key,
            livekit_api_secret=secret,
            ignored_words=ignored_list,
            confidence_limit=conf_limit,
            allow_dynamic_updates=dynamic_update,
            min_interrupt_time=min_interrupt,
            false_interrupt_delay=false_delay,
            resume_on_false=resume_false
        )

    def validate(self) -> bool:
        """
        Before running my agent, I call this method to make sure all settings
        make sense. If something looks wrong, I raise an error immediately.
        """
        # Check that my LiveKit credentials are present.
        if not self.livekit_url:
            raise ValueError("LIVEKIT_URL is missing from the environment.")
        if not self.livekit_api_key:
            raise ValueError("LIVEKIT_API_KEY is missing from the environment.")
        if not self.livekit_api_secret:
            raise ValueError("LIVEKIT_API_SECRET is missing from the environment.")

        # The confidence limit should always stay between 0 and 1.
        if not 0.0 <= self.confidence_limit <= 1.0:
            raise ValueError("CONFIDENCE_THRESHOLD must be between 0.0 and 1.0")

        # I make sure all timing values are positive to avoid runtime issues.
        if self.min_interrupt_time < 0:
            raise ValueError("MIN_INTERRUPTION_DURATION cannot be negative.")
        if self.false_interrupt_delay < 0:
            raise ValueError("FALSE_INTERRUPTION_TIMEOUT cannot be negative.")

        # Everything looks good if we reach this point.
        return True
