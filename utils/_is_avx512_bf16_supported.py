
def _is_avx512_bf16_supported() -> bool:
    r"""Returns a bool indicating if CPU supports AVX512_BF16."""
    return get_capabilities().get("avx512_bf16", False)

