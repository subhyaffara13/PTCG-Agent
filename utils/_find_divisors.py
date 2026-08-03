import math


def _find_divisors(size: int):
  """Fast-ish method for finding divisors of a number."""
  sqrt_divs = [
      i for i in range(1, math.ceil(math.sqrt(size + 1))) if size % i == 0
  ]
  return sorted(set(sqrt_divs + [size // div for div in sqrt_divs][::-1]))

