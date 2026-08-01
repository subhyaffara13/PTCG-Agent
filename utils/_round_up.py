
def _round_up(x: int, y: int) -> int:
    """Round x up to the nearest multiple of y."""
    return ((x + y - 1) // y) * y


def _round_up(i, n):
  return ((i+n-1) // n) * n

