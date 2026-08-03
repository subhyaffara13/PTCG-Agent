import sys

def normalize_path_separators(path: str) -> str:
    return path.replace("\\", "/") if sys.platform == "win32" else path

