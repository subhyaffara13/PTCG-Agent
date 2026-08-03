import sys

def _supports_raw_keyboard() -> bool:
    if not (sys.stdin and sys.stdin.isatty() and sys.stdout.isatty()):
        return False
    if sys.platform == "win32":
        return _enable_windows_vt_processing()
    return True

