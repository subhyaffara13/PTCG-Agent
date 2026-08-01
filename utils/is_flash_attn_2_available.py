
def is_flash_attn_2_available() -> bool:
    is_available, flash_attn_version = _is_package_available("flash_attn", return_version=True)
    # FA4 is also distributed under "flash_attn", hence we need to check the naming here
    is_available = is_available and "flash-attn" in [
        pkg.replace("_", "-") for pkg in PACKAGE_DISTRIBUTION_MAPPING.get("flash_attn", [])
    ]

    if not is_available or not (is_torch_cuda_available() or is_torch_mlu_available()):
        return False

    # Only allow versions >= 2.3.3 to avoid very old legacy workarounds that are now 2+ years old
    try:
        return version.parse(flash_attn_version) >= version.parse("2.3.3")
    except packaging.version.InvalidVersion:
        return False

