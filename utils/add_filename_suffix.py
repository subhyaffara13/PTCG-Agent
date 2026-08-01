
def add_filename_suffix(file_path: str, suffix: str) -> str:
    """
    Append a suffix at the filename (before the extension).
    Args:
        path: pathlib.Path The actual path object we would like to add a suffix
        suffix: The suffix to add
    Returns: path with suffix appended at the end of the filename and before extension
    """
    path = Path(file_path)
    return str(path.parent.joinpath(path.stem + suffix).with_suffix(path.suffix))

