
def require_flash_attn(test_case):
    """
    Decorator marking a test that requires Flash Attention.

    These tests are skipped when Flash Attention isn't installed.

    """
    flash_attn_available = is_flash_attn_2_available()
    kernels_available = is_kernels_available()
    try:
        from kernels import get_kernel

        get_kernel(FLASH_ATTN_KERNEL_FALLBACK["flash_attention_2"])
    except Exception as _:
        kernels_available = False

    return unittest.skipUnless(kernels_available | flash_attn_available, "test requires Flash Attention")(test_case)

