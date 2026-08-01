
def python_version() -> Version:
    """
    Return a PEP-440-style version for the current Python interpreter.

    This is more rigorous than `platform.python_version`, which can include
    non-PEP-440-compatible data.
    """
    info = sys.version_info
    return Version(f"{info.major}.{info.minor}.{info.micro}")

