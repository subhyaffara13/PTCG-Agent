
def is_bitsandbytes_available(min_version: str = BITSANDBYTES_MIN_VERSION) -> bool:
    is_available, bitsandbytes_version = _is_package_available("bitsandbytes", return_version=True)
    return is_available and version.parse(bitsandbytes_version) >= version.parse(min_version)

