
def require_flash_attn_4(test_case):
    """
    Decorator marking a test that requires Flash Attention 4.

    These tests are skipped when Flash Attention 4 isn't installed.
    """
    return unittest.skipUnless(is_flash_attn_4_available(), "test requires Flash Attention 4")(test_case)

