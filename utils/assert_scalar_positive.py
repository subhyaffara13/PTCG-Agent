
def assert_scalar_positive(x: Scalar) -> None:
  """Checks that a scalar is positive.

  Args:
    x: A value to check.

  Raises:
    AssertionError: If ``x`` is not a scalar or strictly positive.
  """
  assert_scalar(x)
  if x <= 0:
    raise AssertionError(f"The argument must be positive, got {x}.")

