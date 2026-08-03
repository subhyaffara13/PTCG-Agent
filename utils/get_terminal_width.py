import os

def get_terminal_width() -> int:
    """Get current terminal width if possible, otherwise return the default one."""
    return (
        int(os.getenv("MYPY_FORCE_TERMINAL_WIDTH", "0"))
        or shutil.get_terminal_size().columns
        or DEFAULT_COLUMNS
    )


def get_terminal_width() -> int:
    width, _ = shutil.get_terminal_size(fallback=(80, 24))

    # The Windows get_terminal_size may be bogus, let's sanify a bit.
    if width < 40:
        width = 80

    return width

