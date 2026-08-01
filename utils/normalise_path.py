
def normalise_path(path: str) -> str:
    path = os.path.splitdrive(path)[1]
    path = path.replace(os.sep, "/")
    return path

