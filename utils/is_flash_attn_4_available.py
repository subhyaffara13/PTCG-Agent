
def is_flash_attn_4_available() -> bool:
    is_available = _is_package_available("flash_attn")[0]
    # FA2 is also distributed under "flash_attn", hence we need to check the naming here
    # NOTE: FA2 seems to distribute the `cute` subdirectory even if only FA2 has been installed
    #       -> check for the proper (normalized) distribution name
    is_available = is_available and "flash-attn-4" in [
        pkg.replace("_", "-") for pkg in PACKAGE_DISTRIBUTION_MAPPING.get("flash_attn", [])
    ]

    return is_available and is_torch_cuda_available()

