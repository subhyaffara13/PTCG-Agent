
def is_freethreaded():
    """Return True if the Python interpreter is built with free threading support."""
    return bool(sysconfig.get_config_var('Py_GIL_DISABLED'))

