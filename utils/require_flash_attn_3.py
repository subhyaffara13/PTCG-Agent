
def require_flash_attn_3(test_case):
    """
    Decorator marking a test that requires Flash Attention 3.

    These tests are skipped when Flash Attention 3 isn't installed.
    """
    return unittest.skipUnless(is_flash_attn_3_available(), "test requires Flash Attention 3")(test_case)

