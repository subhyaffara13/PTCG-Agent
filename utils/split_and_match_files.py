
def split_and_match_files(paths: str) -> list[str]:
    """Take a string representing a list of files/directories (with support for globbing
    through the glob library).

    Where a path/glob matches no file, we still include the raw path in the resulting list.

    Returns a list of file paths
    """

    return split_and_match_files_list(split_commas(paths))

