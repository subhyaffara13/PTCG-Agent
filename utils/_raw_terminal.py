import sys

def _raw_terminal():
    """Put the terminal in cbreak mode (read keypresses without Enter). No-op on Windows."""
    if sys.platform == "win32":
        yield
        return

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

