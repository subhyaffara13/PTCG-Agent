
def numpy_supports_type_hints() -> bool:
    """Returns True if numpy supports type hints."""
    np_ver = _get_numpy_version()
    return np_ver and np_ver > NUMPY_VERSION_TYPE_HINTS_SUPPORT

