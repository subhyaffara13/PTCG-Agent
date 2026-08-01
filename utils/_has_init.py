
def _has_init(directory: str) -> str | None:
    """If the given directory has a valid __init__ file, return its path,
    else return None.
    """
    mod_or_pack = os.path.join(directory, "__init__")
    for ext in (*PY_SOURCE_EXTS, "pyc", "pyo"):
        if os.path.exists(mod_or_pack + "." + ext):
            return mod_or_pack + "." + ext
    return None

