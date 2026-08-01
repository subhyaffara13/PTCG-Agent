
def require_flash_linear_attention(test_case):
    """
    Decorator marking a test that requires Flash Linear Attention.

    These tests are skipped when Flash Linear Attention isn't installed.
    """

    return unittest.skipUnless(
        is_flash_linear_attention_available(),
        "test requires `flash-linear-attention`",
    )(test_case)

