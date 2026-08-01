
def next_power_of_2(n: int) -> int:
    """Return the smallest power of 2 greater than or equal to n"""
    if isinstance(n, sympy.Integer):
        n = int(n)
    if n <= 0:
        return 1
    return 1 << (n - 1).bit_length()


def next_power_of_2(x: int) -> int:
  """Returns the next power of two greater than or equal to `x`."""
  if x < 0:
    raise ValueError("`next_power_of_2` requires a non-negative integer.")
  return 1 if x == 0 else 2 ** (x - 1).bit_length()


def next_power_of_2(x: int):
  """Finds the smallest power of 2 >= x using bit manipulation.

  Args:
    x: The input number (should be an integer).

  Returns:
    The smallest integer power of 2 that is >= x.
  """
  assert x > 0
  if x == 1:
    return 1
  return 1 << (x - 1).bit_length()

