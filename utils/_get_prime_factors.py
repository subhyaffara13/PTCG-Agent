import math


def _get_prime_factors(x: int) -> list[int]:
  """Returns a sorted list of prime factors for the given number."""
  assert x > 0
  factors = []
  for p in range(2, math.isqrt(x) + 2):
    while x % p == 0:
      factors.append(p)
      x //= p
    if x == 1:
      return factors
  else:
    return [x]  # x is a prime number.

