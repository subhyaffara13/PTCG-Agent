
def _get_terminal_width(default=80):
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return default

