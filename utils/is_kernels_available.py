
def is_kernels_available(MIN_VERSION: str = KERNELS_MIN_VERSION) -> bool:
    is_available, kernels_version = _is_package_available("kernels", return_version=True)
    return is_available and version.parse(kernels_version) >= version.parse(MIN_VERSION)

