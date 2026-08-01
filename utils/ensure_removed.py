
def ensure_removed(obj, attr) -> Generator[None, None, None]:
    """Ensure that an attribute added to 'obj' during the test is
    removed when we're done
    """
    try:
        yield
    finally:
        try:
            delattr(obj, attr)
        except AttributeError:
            pass
        obj._accessors.discard(attr)

