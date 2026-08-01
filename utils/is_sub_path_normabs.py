
def is_sub_path_normabs(path: str, dir: str) -> bool:
    """Given two paths, return if path is a sub-path of dir.

    Moral equivalent of: Path(dir) in Path(path).parents

    Similar to the pathlib version:
    - Treats paths case-sensitively
    - Does not fully handle unnormalised paths (e.g. paths with "..")
    - Does not handle a mix of absolute and relative paths
    Unlike the pathlib version:
    - Fast
    - On Windows, assumes input has been slash normalised
    - Handles even fewer unnormalised paths (e.g. paths with "." and "//")

    As a result, callers should ensure that inputs have had os.path.abspath called on them
    (note that os.path.abspath will normalise)
    """
    if not dir.endswith(os.sep):
        dir += os.sep
    return path.startswith(dir)

