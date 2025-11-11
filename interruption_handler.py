"""
In this file, I’ve built the logic that decides whether the user’s speech
should interrupt the agent or be ignored as harmless filler.
It filters out low-confidence audio and common hesitation words in real time.
"""

import logging
import re
from dataclasses import dataclass
from typing import List, Set, Optional

log = logging.getLogger(__name__)


@dataclass
class InterruptionConfig:
    """
    I use this dataclass to define how my interruption filter behaves.
    It lets me specify which words I want to ignore and how strict I want
    the confidence filter to be.
    """
    ignored_words: Set[str]
    confidence_limit: float = 0.5
    allow_dynamic_updates: bool = False

    @classmethod
    def from_word_list(cls, words: List[str],
                       confidence_limit: float = 0.5,
                       allow_dynamic_updates: bool = False) -> 'InterruptionConfig':
        """
        Here I normalize and store my filler words list in lowercase so
        comparison during runtime becomes easy and case-insensitive.
        """
        cleaned = {w.strip().lower() for w in words if w.strip()}
        return cls(ignored_words=cleaned,
                   confidence_limit=confidence_limit,
                   allow_dynamic_updates=allow_dynamic_updates)


class InterruptionHandler:
    """
    I created this class to make my voice agent smarter about interruptions.
    It helps me skip over meaningless sounds like “uh”, “umm”, and “haan”
    without letting them pause my agent mid-sentence.
    """

    def __init__(self, config: InterruptionConfig):
        """
        When I initialize this class, I take in my configuration object and
        prepare my internal data so I can evaluate user speech efficiently.
        """
        self.cfg = config
        self._ignored = config.ignored_words.copy()
        self._threshold = config.confidence_limit
        self._can_update = config.allow_dynamic_updates

        log.info(f"I set up my handler with {len(self._ignored)} ignored words "
                 f"and confidence limit {self._threshold}")

    def should_ignore_speech(self, text: str, confidence: Optional[float] = None) -> bool:
        """
        This is where I decide if a given piece of transcribed speech should
        be ignored. I consider both the ASR confidence and the word content.
        """
        # If the speech confidence is too low, I simply discard it.
        if confidence is not None and confidence < self._threshold:
            log.debug(f"I’m skipping low-confidence text: '{text}' ({confidence:.2f})")
            return True

        # I clean the text to make it easier to analyze.
        normalized = self._normalize(text)

        # Empty or whitespace-only text shouldn’t be treated as meaningful.
        if not normalized:
            log.debug(f"I’m ignoring empty or non-alphanumeric text: '{text}'")
            return True

        words = normalized.split()

        # I keep only the non-filler words to decide if it’s real speech.
        non_fillers = [w for w in words if w not in self._ignored]

        # If all the words were fillers, this segment isn’t a true interruption.
        if not non_fillers:
            log.debug(f"I’m ignoring filler-only speech: {words}")
            return True

        # Otherwise, it’s something meaningful and must interrupt the agent.
        log.debug(f"I recognized meaningful words: {non_fillers}")
        return False

    def _normalize(self, text: str) -> str:
        """
        I normalize text by lowering case, removing punctuation, and stripping
        extra spaces so my word matching works reliably across transcripts.
        """
        cleaned = re.sub(r'[^a-z0-9\s]', '', text.lower())
        return ' '.join(cleaned.split())

    def add_ignored_word(self, word: str):
        """
        I can add new filler words while running if dynamic updates are enabled.
        This lets me adapt to user behavior or multiple languages on the fly.
        """
        if not self._can_update:
            log.warning("Dynamic updates are disabled, so I can’t add new words.")
            return
        w = word.strip().lower()
        if w and w not in self._ignored:
            self._ignored.add(w)
            log.info(f"I added '{w}' to my ignored words list.")

    def remove_ignored_word(self, word: str):
        """
        I can also remove a word from my filler list if I realize it’s actually
        meaningful in a given conversation.
        """
        if not self._can_update:
            log.warning("Dynamic updates are disabled, so I can’t remove words.")
            return
        w = word.strip().lower()
        if w in self._ignored:
            self._ignored.remove(w)
            log.info(f"I removed '{w}' from my ignored words list.")

    def get_ignored_words(self) -> Set[str]:
        """I return the current list of ignored (filler) words."""
        return self._ignored.copy()

    def update_confidence_threshold(self, new_value: float):
        """
        If I want to make my filter stricter or more lenient, I can update
        the confidence threshold safely within the 0.0–1.0 range.
        """
        if not 0.0 <= new_value <= 1.0:
            raise ValueError("Confidence threshold must be between 0.0 and 1.0")
        old = self._threshold
        self._threshold = new_value
        log.info(f"I changed confidence threshold from {old:.2f} to {new_value:.2f}")

    def get_stats(self) -> dict:
        """Here I summarize my current configuration and runtime state."""
        return {
            "ignored_words_count": len(self._ignored),
            "confidence_threshold": self._threshold,
            "dynamic_updates_enabled": self._can_update,
            "ignored_words": sorted(self._ignored)
        }
