
def is_liger_kernel_available() -> bool:
    is_available, liger_kernel_version = _is_package_available("liger_kernel", return_version=True)
    return is_available and version.parse(liger_kernel_version) >= version.parse("0.3.0")

