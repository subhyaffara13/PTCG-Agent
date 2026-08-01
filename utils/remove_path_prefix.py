
def remove_path_prefix(path: str, prefix: str | None) -> str:
    """If path starts with prefix, return copy of path with the prefix removed.
    Otherwise, return path. If path is None, return None.
    """
    if prefix is not None and path.startswith(prefix):
        return path[len(prefix) :]
    else:
        return path

