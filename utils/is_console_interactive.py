import sys

def is_console_interactive() -> bool:
    """Is this console interactive?"""
    return sys.stdin is not None and sys.stdin.isatty()

