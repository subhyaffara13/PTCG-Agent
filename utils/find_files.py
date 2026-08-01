
def find_files(path: str, pattern: str) -> list[str]:
    """Returns a list of absolute paths of files beneath path, recursively,
    with filenames which match the UNIX-style shell glob pattern."""
    result: list[str] = []
    for root, _, files in os.walk(path):
        matches = fnmatch.filter(files, pattern)
        result.extend(os.path.join(root, f) for f in matches)
    return result

