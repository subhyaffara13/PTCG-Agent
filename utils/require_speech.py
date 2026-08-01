
def require_speech(test_case):
    """
    Decorator marking a test that requires speech. These tests are skipped when speech isn't available.
    """
    return unittest.skipUnless(is_speech_available(), "test requires torchaudio")(test_case)

