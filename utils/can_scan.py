import sys

def can_scan() -> bool:
    if not sys.platform.startswith('java') and sys.platform != 'cli':
        # CPython, PyPy, etc.
        return True
    log.warn("Unable to analyze compiled code on this platform.")
    log.warn(
        "Please ask the author to include a 'zip_safe'"
        " setting (either True or False) in the package's setup.py"
    )
    return False

