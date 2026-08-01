
def split_and_match_files_list(paths: Sequence[str]) -> list[str]:
    """Take a list of files/directories (with support for globbing through the glob library).

    Where a path/glob matches no file, we still include the raw path in the resulting list.

    Returns a list of file paths
    """
    expanded_paths = []

    for path in paths:
        path = expand_path(path.strip())
        globbed_files = fileglob.glob(path, recursive=True)
        if globbed_files:
            expanded_paths.extend(globbed_files)
        else:
            expanded_paths.append(path)

    return expanded_paths

