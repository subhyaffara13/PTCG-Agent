
def _pytest_has_xdist():
    """
    Check if the pytest-xdist plugin is installed, providing parallel tests
    """
    # Check xdist exists without importing, otherwise pytests emits warnings
    from importlib.util import find_spec
    return find_spec('xdist') is not None

