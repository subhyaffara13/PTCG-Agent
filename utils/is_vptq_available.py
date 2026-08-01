
def is_vptq_available(min_version: str = VPTQ_MIN_VERSION) -> bool:
    is_available, vptq_version = _is_package_available("vptq", return_version=True)
    return is_available and version.parse(vptq_version) >= version.parse(min_version)

