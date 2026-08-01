
def _get_relative_base_path(filename: str, path_to_check: str) -> list[str] | None:
    """Extracts the relative mod path of the file to import from.

    Check if a file is within the passed in path and if so, returns the
    relative mod path from the one passed in.

    If the filename is no in path_to_check, returns None

    Note this function will look for both abs and realpath of the file,
    this allows to find the relative base path even if the file is a
    symlink of a file in the passed in path

    Examples:
        _get_relative_base_path("/a/b/c/d.py", "/a/b") ->  ["c","d"]
        _get_relative_base_path("/a/b/c/d.py", "/dev") ->  None
    """
    path_to_check = os.path.normcase(os.path.normpath(path_to_check))

    abs_filename = os.path.abspath(filename)
    if _is_subpath(abs_filename, path_to_check):
        base_path = os.path.splitext(abs_filename)[0]
        relative_base_path = base_path[len(path_to_check) :].lstrip(os.path.sep)
        return [pkg for pkg in relative_base_path.split(os.sep) if pkg]

    real_filename = os.path.realpath(filename)
    if _is_subpath(real_filename, path_to_check):
        base_path = os.path.splitext(real_filename)[0]
        relative_base_path = base_path[len(path_to_check) :].lstrip(os.path.sep)
        return [pkg for pkg in relative_base_path.split(os.sep) if pkg]

    return None

