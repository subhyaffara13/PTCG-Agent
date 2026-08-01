
def is_flash_attn_greater_or_equal(library_version: str) -> bool:
    is_available, flash_attn_version = _is_package_available("flash_attn", return_version=True)
    # FA4 is also distributed under "flash_attn", hence we need to check the naming here
    is_available = is_available and "flash-attn" in [
        pkg.replace("_", "-") for pkg in PACKAGE_DISTRIBUTION_MAPPING.get("flash_attn", [])
    ]

    if not is_available:
        return False
    try:
        return version.parse(flash_attn_version) >= version.parse(library_version)
    except packaging.version.InvalidVersion:
        return False

