
def abspath(path: str) -> str:
    # FS objects have no concept of a *current directory*. This simply
    # ensures the path starts with a forward slash.
    if not path.startswith("/"):
        return "/" + path
    return path

