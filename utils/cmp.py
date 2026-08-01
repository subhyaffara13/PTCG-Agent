
def cmp(a: int, b: int) -> int:
    return int(a > b) - int(a < b)


def cmp(a: float, b: float) -> int:
    return (a > b) - (a < b)


def cmp(a, b):
    """Returns 1 if a > b, otherwise returns -1."""
    return (a > b).astype(int) - (a < b).astype(int)


def cmp(a, b):
    return float(a > b) - float(a < b)


def cmp(a, b):
    return float(a > b) - float(a < b)

