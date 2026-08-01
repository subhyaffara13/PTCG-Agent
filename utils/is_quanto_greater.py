
def is_quanto_greater(library_version: str, accept_dev: bool = False) -> bool:
    """
    Accepts a library version and returns True if the current version of the library is greater than or equal to the
    given version. If `accept_dev` is True, it will also accept development versions (e.g. 2.7.0.dev20250320 matches
    2.7.0).
    """
    if not is_optimum_quanto_available():
        return False

    _, quanto_version = _is_package_available("optimum.quanto", return_version=True)
    if accept_dev:
        return version.parse(version.parse(quanto_version).base_version) > version.parse(library_version)
    else:
        return version.parse(quanto_version) > version.parse(library_version)

