
def assert_scalar(x: Scalar) -> None:
  """Checks that ``x`` is a scalar, as defined in `pytypes.py` (int or float).

  Args:
    x: An object to check.

  Raises:
    AssertionError: If ``x`` is not a scalar as per definition in pytypes.py.
  """
  if not isinstance(x, (int, float)):
    raise AssertionError(f"The argument {x} must be a scalar, got {type(x)}.")

