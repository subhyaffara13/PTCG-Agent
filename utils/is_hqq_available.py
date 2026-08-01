
def is_hqq_available(min_version: str = HQQ_MIN_VERSION) -> bool:
    is_available, hqq_version = _is_package_available("hqq", return_version=True)
    return is_available and version.parse(hqq_version) >= version.parse(min_version)

