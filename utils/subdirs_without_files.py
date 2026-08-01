
def subdirs_without_files(path: str) -> Generator[Path]:
    """Yields every subdirectory of +path+ that has no files under it."""
    return _subdirs_without_generic(path, lambda root, filenames: len(filenames) > 0)

