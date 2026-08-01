
def path_match_suffix_ignore_case(path: pathlib.Path | str, suffix: str) -> bool:
    """
    Returns whether `path` ends in `suffix`, ignoring case.
    """
    if not isinstance(path, str):
        path = str(path)
    return path.casefold().endswith(suffix.casefold())

