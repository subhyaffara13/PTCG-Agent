
def assert_scalar_non_negative(x: Scalar) -> None:
  """Checks that a scalar is non-negative.

  Args:
    x: A value to check.

  Raises:
    AssertionError: If ``x`` is not a scalar or negative.
  """
  assert_scalar(x)
  if x < 0:
    raise AssertionError(f"The argument must be non-negative, was {x}.")

