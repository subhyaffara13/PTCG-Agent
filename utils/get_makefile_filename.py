
def get_makefile_filename() -> str:
    """Return full pathname of installed Makefile from the Python build."""
    return sysconfig.get_makefile_filename()

