
def _is_avx2_supported() -> bool:
    r"""Returns a bool indicating if CPU supports AVX2."""
    return get_capabilities().get("avx2", False)

