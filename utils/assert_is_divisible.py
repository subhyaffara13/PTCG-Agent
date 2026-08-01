
def assert_is_divisible(numerator: int, denominator: int) -> None:
  """Checks that ``numerator`` is divisible by ``denominator``.

  Args:
    numerator: A numerator.
    denominator: A denominator.

  Raises:
    AssertionError: If ``numerator`` is not divisible by ``denominator``.
  """
  if numerator % denominator != 0:
    raise AssertionError(f"{numerator} is not divisible by {denominator}.")

