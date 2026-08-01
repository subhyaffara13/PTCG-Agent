
def convert_oserror(exc, pid=None, name=None):
    """Convert OSError into NoSuchProcess or AccessDenied."""
    assert isinstance(exc, OSError), exc
    if is_permission_err(exc):
        return AccessDenied(pid=pid, name=name)
    if isinstance(exc, ProcessLookupError):
        return NoSuchProcess(pid=pid, name=name)
    raise exc

