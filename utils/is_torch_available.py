
def is_torch_available() -> bool:
    try:
        is_available, torch_version = _is_package_available("torch", return_version=True)
        parsed_version = version.parse(torch_version)
        if is_available and parsed_version < version.parse("2.4.0"):
            logger.warning_once(f"Disabling PyTorch because PyTorch >= 2.4 is required but found {torch_version}")
        return is_available and version.parse(torch_version) >= version.parse("2.4.0")
    except packaging.version.InvalidVersion:
        return False


def is_torch_available() -> bool:
    return is_package_available("torch")

