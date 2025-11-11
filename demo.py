"""
I use this script to interactively demonstrate how my interruption handler
behaves across a variety of realistic scenarios: filler-only speech,
mixed utterances, low-confidence ASR, background murmur, and multilingual cases.
"""

from interruption_handler import InterruptionHandler, InterruptionConfig


def _print_banner(title: str):
    """I print a simple banner to organize demo output."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def _run_case(handler: InterruptionHandler, text: str, confidence: float | None = None, note: str = ""):
    """
    I evaluate a single demo case and print whether I would ignore the input
    or treat it as a valid interruption.
    """
    should_ignore = handler.should_ignore_speech(text, confidence)
    conf_part = f" (confidence: {confidence:.2f})" if confidence is not None else ""
    status = "🔇 IGNORED" if should_ignore else "✅ PROCESSED"
    print(f"{status} | '{text}'{conf_part}")
    if note:
        print(f"    └─ {note}")
    print()


def main():
    """I run a set of curated scenarios to showcase handler behavior."""
    cfg = InterruptionConfig.from_word_list(
        words=["uh", "umm", "hmm", "haan", "um", "er", "ah"],
        confidence_limit=0.5,
        allow_dynamic_updates=True
    )
    handler = InterruptionHandler(cfg)

    print("\n🎧 Live demo: Interruption Handler\n")

    _print_banner("Configuration")
    print(f"Ignored words: {sorted(handler.get_ignored_words())}")
    print(f"Confidence threshold: {cfg.confidence_limit}\n")

    _print_banner("Scenario 1 — Filler-only Speech (Agent speaking)")
    _run_case(handler, "uh", note="single filler")
    _run_case(handler, "umm", note="single filler")
    _run_case(handler, "uh umm hmm", note="multiple fillers")
    _run_case(handler, "Uh, umm... hmm!", note="fillers with punctuation")

    _print_banner("Scenario 2 — Clear Interruptions (Agent speaking)")
    _run_case(handler, "wait", note="explicit command")
    _run_case(handler, "stop", note="explicit command")
    _run_case(handler, "hold on a second", note="multi-word command")
    _run_case(handler, "I have a question", note="complete sentence")

    _print_banner("Scenario 3 — Mixed Filler + Command")
    _run_case(handler, "umm okay stop", note="filler then command")
    _run_case(handler, "uh wait a minute", note="filler then request")
    _run_case(handler, "hmm i think so", note="filler then thought")

    _print_banner("Scenario 4 — Confidence-Based Filtering")
    _run_case(handler, "hello", confidence=0.2, note="very low confidence")
    _run_case(handler, "hello", confidence=0.4, note="low confidence (still below threshold)")
    _run_case(handler, "hello", confidence=0.6, note="above threshold")
    _run_case(handler, "hello", confidence=0.95, note="very high confidence")

    _print_banner("Scenario 5 — Background & Murmur")
    _run_case(handler, "hmm yeah", confidence=0.3, note="low-confidence background murmur")
    _run_case(handler, "uh huh", confidence=0.4, note="acknowledgment sound low confidence")
    _run_case(handler, "", note="silence/empty input")
    _run_case(handler, "...", note="punctuation only")

    _print_banner("Scenario 6 — Multilingual Fillers")
    _run_case(handler, "haan", note="Hindi filler")
    _run_case(handler, "uh haan", note="mixed-language filler sequence")
    _run_case(handler, "namaste", note="real Hindi word - should be processed")

    _print_banner("Scenario 7 — Edge Cases")
    _run_case(handler, "UH", note="uppercase filler")
    _run_case(handler, "Umm", note="mixed case filler")
    _run_case(handler, "   ", note="whitespace only")
    _run_case(handler, "uh!", note="filler with punctuation token")

    _print_banner("Dynamic Updates Demo (optional)")
    # Demonstrate dynamic updates if enabled
    if cfg.allow_dynamic_updates:
        print("I will add 'hmm2' as a filler word and then test it.")
        handler.add_ignored_word("hmm2")
        _run_case(handler, "hmm2", note="newly-added filler (runtime update)")
        handler.remove_ignored_word("hmm2")
        print("I removed 'hmm2' again.\n")
    else:
        print("Dynamic updates are not enabled in the current configuration.\n")

    _print_banner("Summary")
    stats = handler.get_stats()
    print(f"Ignored words count: {stats['ignored_words_count']}")
    print(f"Confidence threshold: {stats['confidence_threshold']}")
    print(f"Dynamic updates enabled: {stats['dynamic_updates_enabled']}")
    print("\n✨ Demo finished. I verified the handler's behaviour across scenarios.\n")


if __name__ == "__main__":
    main()
