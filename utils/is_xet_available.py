
def is_xet_available() -> bool:
    # since hf_xet is automatically used if available, allow explicit disabling via environment variable
    if constants.HF_HUB_DISABLE_XET:
        return False

    return is_package_available("hf_xet")

