import sys

def stdin_get_value():
    """Read the value from stdin."""
    return io.TextIOWrapper(sys.stdin.buffer, errors='ignore').read()


def stdin_get_value() -> str:
    """Get and cache it so plugins can use it."""
    stdin_value = sys.stdin.buffer.read()
    fd = io.BytesIO(stdin_value)
    try:
        coding, _ = tokenize.detect_encoding(fd.readline)
        fd.seek(0)
        return io.TextIOWrapper(fd, coding).read()
    except (LookupError, SyntaxError, UnicodeError):
        return stdin_value.decode("utf-8")

