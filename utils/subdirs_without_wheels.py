
def subdirs_without_wheels(path: str) -> Generator[Path]:
    """Yields every subdirectory of +path+ that has no .whl files under it."""
    return _subdirs_without_generic(
        path, lambda root, filenames: any(x.endswith(".whl") for x in filenames)
    )

