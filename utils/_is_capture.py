
def _is_capture(action_string: str) -> bool:
    """A checkers capture jumps two ranks (e.g. d6b4); a slide moves one."""
    if len(action_string) != 4:
        return False
    try:
        return abs(int(action_string[1]) - int(action_string[3])) == 2
    except ValueError:
        return False

