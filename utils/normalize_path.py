
def normalize_path(path: str, parent: str = os.curdir) -> str:
    """Normalize a single-path.

    :returns:
        The normalized path.
    """
    # NOTE(sigmavirus24): Using os.path.sep and os.path.altsep allow for
    # Windows compatibility with both Windows-style paths (c:\foo\bar) and
    # Unix style paths (/foo/bar).
    separator = os.path.sep
    # NOTE(sigmavirus24): os.path.altsep may be None
    alternate_separator = os.path.altsep or ""
    if (
        path == "."
        or separator in path
        or (alternate_separator and alternate_separator in path)
    ):
        path = os.path.abspath(os.path.join(parent, path))
    return path.rstrip(separator + alternate_separator)


def normalize_path(path: str) -> str:
    """
    Drop "." and ".." segments from a URL path.

    For example:

        normalize_path("/path/./to/somewhere/..") == "/path/to"
    """
    # Fast return when no '.' characters in the path.
    if "." not in path:
        return path

    components = path.split("/")

    # Fast return when no '.' or '..' components in the path.
    if "." not in components and ".." not in components:
        return path

    # https://datatracker.ietf.org/doc/html/rfc3986#section-5.2.4
    output: list[str] = []
    for component in components:
        if component == ".":
            pass
        elif component == "..":
            if output and output != [""]:
                output.pop()
        else:
            output.append(component)
    return "/".join(output)


def normalize_path(filename: StrPath) -> str: ...


def normalize_path(filename: BytesPath) -> bytes: ...


def normalize_path(filename: StrOrBytesPath) -> str | bytes:
    """Normalize a file/dir name for comparison purposes"""
    return os.path.normcase(os.path.realpath(os.path.normpath(_cygwin_patch(filename))))


def normalize_path(path: str) -> str:
    # Drop '.' and '..' from str path
    prefix = ""
    if path and path[0] == "/":
        # preserve the "/" root element of absolute paths, copying it to the
        # normalised output as per sections 5.2.4 and 6.2.2.3 of rfc3986.
        prefix = "/"
        path = path[1:]

    segments = path.split("/")
    return prefix + "/".join(normalize_path_segments(segments))


def normalize_path(path: str, resolve_symlinks: bool = True) -> str:
    """
    Convert a path to its canonical, case-normalized, absolute version.

    """
    path = os.path.expanduser(path)
    if resolve_symlinks:
        path = os.path.realpath(path)
    else:
        path = os.path.abspath(path)
    return os.path.normcase(path)

