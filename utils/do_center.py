
def do_center(value: str, width: int = 80) -> str:
    """Centers the value in a field of a given width."""
    return soft_str(value).center(width)

