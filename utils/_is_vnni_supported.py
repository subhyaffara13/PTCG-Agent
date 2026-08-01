
def _is_vnni_supported() -> bool:
    r"""Returns a bool indicating if CPU supports VNNI."""
    # Note: Currently, it only checks avx512_vnni, will add the support of avx2_vnni later.
    return get_capabilities().get("avx512_vnni", False)

