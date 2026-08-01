
def _get_files_from_dir(
    files_dir, included_globs=None, excluded_path_strings=None
):
    if not included_globs:
        included_globs = ["*.py"]
    if not excluded_path_strings:
        excluded_path_strings = []

    files_list = set()
    excluded_files = set()

    for root, _, files in os.walk(files_dir):
        for filename in files:
            path = os.path.join(root, filename)
            if _is_file_included(path, included_globs, excluded_path_strings):
                files_list.add(path)
            else:
                excluded_files.add(path)

    return files_list, excluded_files

