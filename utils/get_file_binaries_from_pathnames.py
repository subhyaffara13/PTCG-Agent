
def get_file_binaries_from_pathnames(
    pathnames: Iterable, mode: str, encoding: str | None = None
):
    if not isinstance(pathnames, Iterable):
        pathnames = [
            pathnames,
        ]

    if mode in ("b", "t"):
        mode = "r" + mode

    for pathname in pathnames:
        if not isinstance(pathname, str):
            raise TypeError(
                f"Expected string type for pathname, but got {type(pathname)}"
            )
        yield pathname, StreamWrapper(open(pathname, mode, encoding=encoding))  # noqa:SIM115

