import os

def get_file_path_2(*path_components: str) -> str:
    return os.path.join(*path_components)

