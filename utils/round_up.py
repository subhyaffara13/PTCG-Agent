
def round_up(x, y):
    """Rounds up x to nearest multiple of y"""
    return ((x + y - 1) // y) * y


def round_up(x: int, y: int) -> int:
    return ((x + y - 1) // y) * y

