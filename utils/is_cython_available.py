
def is_cython_available() -> bool:
    return _is_package_available("pyximport")[0]

