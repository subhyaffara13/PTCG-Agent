
def is_python_source(filename: str | None) -> bool:
    """Return: True if the filename is a python source file."""
    if not filename:
        return False
    return os.path.splitext(filename)[1][1:] in PY_SOURCE_EXTS

