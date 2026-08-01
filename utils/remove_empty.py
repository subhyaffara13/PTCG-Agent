
def remove_empty(fs: FS, path: str):
    """Remove all empty parents."""
    path = PurePosixPath(path)
    root = PurePosixPath("/")
    try:
        while path != root:
            fs.removedir(path.as_posix())
            path = path.parent
    except DirectoryNotEmpty:
        pass

