
def norm_sep(path: str | os.PathLike[str]) -> str:
    """Normalize path separators to forward slashes for nodeid compatibility.

    Replaces backslashes with forward slashes. This handles both Windows native
    paths and cross-platform data (e.g., Windows paths in serialized test reports
    when running on Linux).

    :param path: A path string or PathLike object.
    :returns: String with all backslashes replaced by forward slashes.
    """
    return os.fspath(path).replace("\\", SEP)

