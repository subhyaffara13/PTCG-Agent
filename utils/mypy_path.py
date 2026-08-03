import os

def mypy_path() -> list[str]:
    path_env = os.getenv("MYPYPATH")
    if not path_env:
        return []
    return path_env.split(os.pathsep)

