import os

def highest_init_level(fscache: FileSystemCache, id: str, path: str, prefix: str) -> int:
    """Compute the highest level where an __init__ file is found."""
    if is_init_file(path):
        path = os.path.dirname(path)
    level = 0
    for i in range(id.count(".")):
        path = os.path.dirname(path)
        if any(
            fscache.isfile_case(os_path_join(path, f"__init__{extension}"), prefix)
            for extension in PYTHON_EXTENSIONS
        ):
            level = i + 1
    return level

