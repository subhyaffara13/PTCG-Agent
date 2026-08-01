
def require_all_flash_attn(test_case):
    flash_attn_available = is_flash_attn_2_available()
    kernels_available = is_kernels_available()
    try:
        from kernels import get_kernel

        get_kernel(FLASH_ATTN_KERNEL_FALLBACK["flash_attention_2"])
    except Exception as _:
        kernels_available = False

    return unittest.skipUnless(
        all(
            (
                flash_attn_available | kernels_available,
                is_flash_attn_3_available(),
                is_flash_attn_4_available(),
            )
        ),
        "test requires all mainline Flash Attention packages",
    )(test_case)

