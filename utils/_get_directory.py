
def _get_directory(path: pathlib.Path) -> pathlib.Path:
    """Get the directory of a path - itself if already a directory."""
    if path.is_file():
        return path.parent
    else:
        return path

