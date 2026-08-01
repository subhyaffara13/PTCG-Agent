
def is_sudachi_projection_available() -> bool:
    is_available, sudachipy_version = _is_package_available("sudachipy", return_version=True)
    return is_available and version.parse(sudachipy_version) >= version.parse("0.6.8")

