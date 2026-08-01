
def make_module_path_relative(abs_path: str) -> str:
    """
    Given an absolute filepath corresponding to a Python module which was
    loaded via normal import mechanisms using sys.path, convert it into
    a relative path relative to one of the Python search paths.
    """
    return _make_module_path_relative(abs_path, tuple(sys.path))

