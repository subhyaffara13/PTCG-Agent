
def require_gguf(test_case, min_version: str = GGUF_MIN_VERSION):
    """
    Decorator marking a test that requires ggguf. These tests are skipped when gguf isn't installed.
    """
    return unittest.skipUnless(is_gguf_available(min_version), f"test requires gguf version >= {min_version}")(
        test_case
    )

