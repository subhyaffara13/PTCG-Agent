import os

def _get_unique_path(base_name: str, extension: str) -> str:
    """Get a unique file path, appending a counter if the file already exists.

    For example, if "min_cut_failed.svg" exists, returns "min_cut_failed_1.svg".
    """
    path = f"{base_name}{extension}"
    if not os.path.exists(path):
        return path

    counter = 1
    while os.path.exists(f"{base_name}_{counter}{extension}"):
        counter += 1
    return f"{base_name}_{counter}{extension}"

