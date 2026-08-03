import sys

def term_supports_colors(file=sys.stdout):  # pragma: no cover
    if not hasattr(file, "isatty") or not file.isatty():
        return False
    try:
        file.fileno()
    except Exception:  # noqa: BLE001
        return False
    return True

