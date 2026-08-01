
def assert_scalar_negative(x: Scalar) -> None:
  """Checks that a scalar is negative.

  Args:
    x: A value to check.

  Raises:
    AssertionError: If ``x`` is not a scalar or strictly negative.
  """
  assert_scalar(x)
  if x >= 0:
    raise AssertionError(f"The argument must be negative, was {x}.")

