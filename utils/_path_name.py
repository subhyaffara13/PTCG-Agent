
def _path_name(path: str | None) -> str | None:
    if not path:
        return None
    # If the path is relative it MAY use POSIX-style path separators explicitly
    # for portability
    if "/" in path:
        return path.rsplit("/", 1)[-1]
    elif "\\" in path:
        return path.rsplit("\\", 1)[-1]
    else:
        return path


def _path_name(path: str | None) -> str | None:
    if not path:
        return None
    # If the path is relative it MAY use POSIX-style path separators explicitly
    # for portability
    if "/" in path:
        return path.rsplit("/", 1)[-1]
    elif "\\" in path:
        return path.rsplit("\\", 1)[-1]
    else:
        return path

