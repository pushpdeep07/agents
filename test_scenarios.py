"""
I use this test suite to make sure my interruption handler behaves exactly
as I expect across a range of unit tests. Each test prints a confirmation
message for quick manual verification and uses assertions for automation.
"""

from interruption_handler import InterruptionHandler, InterruptionConfig


def test_filler_only_speech():
    """I confirm that filler-only transcripts are ignored."""
    cfg = InterruptionConfig.from_word_list(["uh", "umm", "hmm"])
    handler = InterruptionHandler(cfg)

    assert handler.should_ignore_speech("uh") is True
    assert handler.should_ignore_speech("umm") is True
    assert handler.should_ignore_speech("uh umm") is True
    assert handler.should_ignore_speech("Uh, umm, hmm") is True

    print("✅ test_filler_only_speech passed")


def test_mixed_speech():
    """I make sure that mixed speech with meaningful words is not ignored."""
    cfg = InterruptionConfig.from_word_list(["uh", "umm", "hmm"])
    handler = InterruptionHandler(cfg)

    assert handler.should_ignore_speech("wait") is False
    assert handler.should_ignore_speech("stop") is False
    assert handler.should_ignore_speech("umm okay stop") is False
    assert handler.should_ignore_speech("uh wait a minute") is False

    print("✅ test_mixed_speech passed")


def test_low_confidence_behavior():
    """I check low-confidence transcripts are filtered based on threshold."""
    cfg = InterruptionConfig.from_word_list(["uh"], confidence_limit=0.5)
    handler = InterruptionHandler(cfg)

    # below threshold -> ignored
    assert handler.should_ignore_speech("hello", confidence=0.3) is True
    assert handler.should_ignore_speech("hello", confidence=0.4) is True

    # above threshold -> processed
    assert handler.should_ignore_speech("hello", confidence=0.6) is False
    assert handler.should_ignore_speech("hello", confidence=0.9) is False

    print("✅ test_low_confidence_behavior passed")


def test_background_murmur_and_threshold():
    """I validate murmur handling and the interplay between fillers and confidence."""
    cfg = InterruptionConfig.from_word_list(["uh", "umm", "hmm", "yeah"], confidence_limit=0.5)
    handler = InterruptionHandler(cfg)

    # low confidence should be ignored regardless of words
    assert handler.should_ignore_speech("hmm yeah", confidence=0.3) is True

    # even with high confidence, if all words are fillers, ignore
    assert handler.should_ignore_speech("hmm yeah", confidence=0.8) is True

    # but real words with high confidence should not be ignored
    assert handler.should_ignore_speech("hello there", confidence=0.8) is False

    print("✅ test_background_murmur_and_threshold passed")


def test_empty_and_punctuation_cases():
    """I ensure that empty or punctuation-only input is ignored safely."""
    cfg = InterruptionConfig.from_word_list(["uh"])
    handler = InterruptionHandler(cfg)

    assert handler.should_ignore_speech("") is True
    assert handler.should_ignore_speech("   ") is True
    assert handler.should_ignore_speech("...") is True
    assert handler.should_ignore_speech("!!!") is True

    print("✅ test_empty_and_punctuation_cases passed")


def test_case_insensitivity_handling():
    """I verify filler matching is case-insensitive."""
    cfg = InterruptionConfig.from_word_list(["uh", "umm"])
    handler = InterruptionHandler(cfg)

    assert handler.should_ignore_speech("UH") is True
    assert handler.should_ignore_speech("Umm") is True
    assert handler.should_ignore_speech("UMM") is True
    assert handler.should_ignore_speech("uH uMm") is True

    print("✅ test_case_insensitivity_handling passed")


def test_dynamic_updates_feature():
    """I test adding/removing filler words at runtime when enabled."""
    cfg = InterruptionConfig.from_word_list(["uh"], allow_dynamic_updates=True)
    handler = InterruptionHandler(cfg)

    # initially 'hmm' should not be treated as filler
    assert handler.should_ignore_speech("hmm") is False

    # add and verify
    handler.add_ignored_word("hmm")
    assert handler.should_ignore_speech("hmm") is True

    # remove and verify
    handler.remove_ignored_word("hmm")
    assert handler.should_ignore_speech("hmm") is False

    print("✅ test_dynamic_updates_feature passed")


def test_multilingual_fillers():
    """I confirm multilingual fillers (like Hindi 'haan') are recognized."""
    cfg = InterruptionConfig.from_word_list(["uh", "umm", "haan", "hmm"])
    handler = InterruptionHandler(cfg)

    assert handler.should_ignore_speech("haan") is True
    assert handler.should_ignore_speech("uh haan") is True
    assert handler.should_ignore_speech("namaste") is False

    print("✅ test_multilingual_fillers passed")


def run_all_tests():
    """I run every test in sequence and report the result."""
    print("\n" + "=" * 60)
    print("Running Interruption Handler Test Suite")
    print("=" * 60 + "\n")

    test_filler_only_speech()
    test_mixed_speech()
    test_low_confidence_behavior()
    test_background_murmur_and_threshold()
    test_empty_and_punctuation_cases()
    test_case_insensitivity_handling()
    test_dynamic_updates_feature()
    test_multilingual_fillers()

    print("\n" + "=" * 60)
    print("All tests passed! ✅")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_tests()
