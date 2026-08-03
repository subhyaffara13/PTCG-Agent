import sys

def _is_interactive() -> bool:
    return sys.stdin.isatty()

