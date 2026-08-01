
def frombase(path1: str, path2: str) -> str:
    # Get the final path of `path2` that isn't in `path1`.
    if not isbase(path1, path2):
        raise ValueError(f"path1 must be a prefix of path2: {path1!r} vs {path2!r}")
    return path2[len(path1) :]

