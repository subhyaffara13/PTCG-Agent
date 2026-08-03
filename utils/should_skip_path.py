import os

def should_skip_path(path: str) -> bool:
    if stats.is_special_module(path):
        return True
    if path.startswith(".."):
        return True
    if "stubs" in path.split("/") or "stubs" in path.split(os.sep):
        return True
    return False

