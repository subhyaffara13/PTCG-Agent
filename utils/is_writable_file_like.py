
def is_writable_file_like(obj):
    """Return whether *obj* looks like a file object with a *write* method."""
    return callable(getattr(obj, 'write', None))

