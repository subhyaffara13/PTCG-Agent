
def _is_file_included(
    path, included_globs, excluded_path_strings, enforce_glob=True
):
    """Determine if a file should be included based on filename

    This utility function determines if a file should be included based
    on the file name, a list of parsed extensions, excluded paths, and a flag
    specifying whether extensions should be enforced.

    :param path: Full path of file to check
    :param parsed_extensions: List of parsed extensions
    :param excluded_paths: List of paths (globbing supported) from which we
        should not include files
    :param enforce_glob: Can set to false to bypass extension check
    :return: Boolean indicating whether a file should be included
    """
    return_value = False

    # if this is matches a glob of files we look at, and it isn't in an
    # excluded path
    if _matches_glob_list(path, included_globs) or not enforce_glob:
        if not _matches_glob_list(path, excluded_path_strings) and not any(
            x in path for x in excluded_path_strings
        ):
            return_value = True

    return return_value

