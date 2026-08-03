import os
import sys

def _read_key() -> str:
    fd = sys.stdin.fileno()
    ch = os.read(fd, 1)
    if ch == b"\x1b":
        if _has_input(fd, 0.05):
            ch2 = os.read(fd, 1)
            if ch2 == b"[" and _has_input(fd, 0.05):
                ch3 = os.read(fd, 1)
                return f"\x1b[{ch3.decode()}"
        return "esc"
    return ch.decode("utf-8", errors="replace")


def _read_key() -> str:
    """Read one keypress, normalizing arrow keys to "up"/"down"."""
    if sys.platform == "win32":
        char = msvcrt.getwch()
        if char in ("\x00", "\xe0"):  # arrow keys come as a two-character sequence
            return {"H": "up", "P": "down"}.get(msvcrt.getwch(), "")
        return char

    # Read the file descriptor directly: `sys.stdin.read(1)` would buffer the whole escape
    # sequence internally, making the fd look empty to `select()` below.
    fd = sys.stdin.fileno()
    char = os.read(fd, 1)
    # Disambiguate a bare Escape from an escape sequence (e.g. "\x1b[A" for Up).
    if char == b"\x1b" and select.select([fd], [], [], 0.05)[0]:
        if os.read(fd, 1) == b"[" and select.select([fd], [], [], 0.05)[0]:
            return {b"A": "up", b"B": "down"}.get(os.read(fd, 1), "")
        return ""
    return char.decode(errors="replace")

