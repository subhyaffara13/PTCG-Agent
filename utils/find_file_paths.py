import os

def find_file_paths(dir_paths: list[str], files_to_exclude: set[str]) -> set[str]:
    """
    When given a path to a directory, returns the paths to the relevant files within it.

    This function does NOT recursive traverse to subdirectories.
    """
    paths: set[str] = set()
    for dir_path in dir_paths:
        all_files = os.listdir(dir_path)
        python_files = {fname for fname in all_files if ".py" == fname[-3:]}
        filter_files = {
            fname for fname in python_files if fname not in files_to_exclude
        }
        paths.update({os.path.join(dir_path, fname) for fname in filter_files})
    return paths

