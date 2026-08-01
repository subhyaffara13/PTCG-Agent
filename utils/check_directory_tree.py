
def check_directory_tree(base_path, file_check, exclusions=set(), pattern="*.py"):
    """
    Checks all files in the directory tree (with base_path as starting point)
    with the file_check function provided, skipping files that contain
    any of the strings in the set provided by exclusions.
    """
    if not base_path:
        return
    for root, dirs, files in walk(base_path):
        check_files(glob(join(root, pattern)), file_check, exclusions)

