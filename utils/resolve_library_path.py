import os

def resolve_library_path(path: str) -> str:
    return os.path.realpath(path)

