import os

def common_dir_prefix(paths: list[str]) -> str:
    if not paths:
        return "."
    cur = os.path.dirname(os.path.normpath(paths[0]))
    for path in paths[1:]:
        while True:
            path = os.path.dirname(os.path.normpath(path))
            if (cur + os.sep).startswith(path + os.sep):
                cur = path
                break
    return cur or "."

