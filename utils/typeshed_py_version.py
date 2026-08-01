
def typeshed_py_version(options: Options) -> tuple[int, int]:
    """Return Python version used for checking whether module supports typeshed."""
    return max(options.python_version, (3, 10))

