
def normalize_path_separator(orig_path: str) -> str:
    if _IS_WINDOWS:
        return orig_path.replace(os.sep, "/")
    return orig_path

