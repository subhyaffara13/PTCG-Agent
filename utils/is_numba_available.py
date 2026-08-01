
def is_numba_available() -> bool:
    is_available = _is_package_available("numba")[0]
    if not is_available:
        return False

    numpy_available, numpy_version = _is_package_available("numpy", return_version=True)
    return not numpy_available or version.parse(numpy_version) < version.parse("2.2.0")

