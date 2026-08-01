
def is_flash_attn_3_available() -> bool:
    # Universally available under `flash_attn_interface`
    is_available = _is_package_available("flash_attn_interface")[0]
    # Resolving and ensuring the proper name of FA3 being associated
    is_available = is_available and "flash-attn-3" in [
        pkg.replace("_", "-") for pkg in PACKAGE_DISTRIBUTION_MAPPING.get("flash_attn_interface", [])
    ]
    return is_available and is_torch_cuda_available()

