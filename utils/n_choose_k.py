import math


def n_choose_k(n, k):
  """Returns the combination choose k among n items."""
  f = math.factorial
  return int(f(n) / f(k) / f(n - k))

