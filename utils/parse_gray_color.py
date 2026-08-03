import sys

def parse_gray_color(cup: bytes) -> str:
    """Reproduce a gray color in ANSI escape sequence"""
    assert sys.platform != "win32", "curses is not available on Windows"
    set_color = "".join([cup[:-1].decode(), "m"])
    gray = curses.tparm(set_color.encode("utf-8"), 1, 9).decode()
    return gray

