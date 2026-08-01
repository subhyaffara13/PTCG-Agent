
def _nest_path(parent: StrPath, path: StrPath) -> str:
    path = parent if path in {".", ""} else os.path.join(parent, path)
    return os.path.normpath(path)

