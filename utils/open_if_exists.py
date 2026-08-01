
def open_if_exists(filename: str, mode: str = "rb") -> t.Optional[t.IO[t.Any]]:
    """Returns a file descriptor for the filename if that file exists,
    otherwise ``None``.
    """
    if not os.path.isfile(filename):
        return None

    return open(filename, mode)

