import os

def _is_subpath(path: str, base: str) -> bool:
    path = os.path.normcase(os.path.normpath(path))
    base = os.path.normcase(os.path.normpath(base))
    if not path.startswith(base):
        return False
    return (len(path) == len(base)) or (path[len(base)] == os.path.sep)

