
def is_permission_err(exc):
    """Return True if this is a permission error."""
    assert isinstance(exc, OSError), exc
    return isinstance(exc, PermissionError) or exc.winerror in {
        cext.ERROR_ACCESS_DENIED,
        cext.ERROR_PRIVILEGE_NOT_HELD,
    }

