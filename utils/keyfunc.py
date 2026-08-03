import os

def keyfunc(name: str) -> tuple[bool, int, str]:
    """Determines sort order for directory listing.

    The desirable properties are:
    1) foo < foo.pyi < foo.py
    2) __init__.py[i] < foo
    """
    base, suffix = os.path.splitext(name)
    for i, ext in enumerate(PY_EXTENSIONS):
        if suffix == ext:
            return (base != "__init__", i, base)
    return (base != "__init__", -1, name)

