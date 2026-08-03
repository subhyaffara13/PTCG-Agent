import os

def is_pyc_only(file: str | None) -> bool:
    return bool(file and file.endswith(".pyc") and not os.path.exists(file[:-1]))

