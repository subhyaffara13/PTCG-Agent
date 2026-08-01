
def is_archive_file(name: str) -> bool:
    """
    Return True if `name` is a considered as an archive file.
    For example:
    >>> assert is_archive_file("foo.whl")
    >>> assert is_archive_file("foo.zip")
    >>> assert is_archive_file("foo.tar.gz")
    >>> assert is_archive_file("foo.tar")
    >>> assert not is_archive_file("foo.tar.baz")
    """
    if not name:
        return False
    ext = splitext(name)[1].lower()
    if ext in ARCHIVE_EXTENSIONS:
        return True
    return False


def is_archive_file(name: str) -> bool:
    """Return True if `name` is a considered as an archive file."""
    ext = splitext(name)[1].lower()
    if ext in ARCHIVE_EXTENSIONS:
        return True
    return False

