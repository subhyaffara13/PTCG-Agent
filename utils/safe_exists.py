
def safe_exists(p: Path) -> bool:
    """Like Path.exists(), but account for input arguments that might be too long (#11394)."""
    try:
        return p.exists()
    except (ValueError, OSError):
        # ValueError: stat: path too long for Windows
        # OSError: [WinError 123] The filename, directory name, or volume label syntax is incorrect
        return False

