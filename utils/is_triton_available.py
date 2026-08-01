
def is_triton_available(min_version: str = TRITON_MIN_VERSION) -> bool:
    is_available, triton_version = _is_package_available("triton", return_version=True)
    return is_available and version.parse(triton_version) >= version.parse(min_version)

