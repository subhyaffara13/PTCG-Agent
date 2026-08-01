
def is_torch_less_or_equal(library_version: str, accept_dev: bool = False) -> bool:
    """
    Accepts a library version and returns True if the current version of the library is less than or equal to the
    given version. If `accept_dev` is True, it will also accept development versions (e.g. 2.7.0.dev20250320 matches
    2.7.0).
    """
    if not is_torch_available():
        return False

    if accept_dev:
        return version.parse(version.parse(get_torch_version()).base_version) <= version.parse(library_version)
    else:
        return version.parse(get_torch_version()) <= version.parse(library_version)

