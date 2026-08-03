import os

def get_file_path(*path_components: str) -> str:
    return os.path.join(torch_parent, *path_components)

