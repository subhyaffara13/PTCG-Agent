
def _is_avx512_supported() -> bool:
    r"""Returns a bool indicating if CPU supports AVX512."""
    return get_capabilities().get("avx512_f", False)

