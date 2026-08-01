
def forcedir(path: str) -> str:
    # Ensure the path ends with a trailing forward slash.
    if not path.endswith("/"):
        return path + "/"
    return path

