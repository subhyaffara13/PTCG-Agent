from typing import Any

def assert_scalar_in(x: Any,
                     min_: Scalar,
                     max_: Scalar,
                     included: bool = True) -> None:
  """Checks that argument is a scalar within segment (by default).

  Args:
    x: An object to check.
    min_: A left border of the segment.
    max_: A right border of the segment.
    included: Whether to include the borders of the segment in the set of
      allowed values.

  Raises:
    AssertionError: If ``x`` is not a scalar; if ``x`` falls out of the segment.
  """
  assert_scalar(x)
  if included:
    if not min_ <= x <= max_:
      raise AssertionError(
          f"The argument must be in [{min_}, {max_}], got {x}.")
  else:
    if not min_ < x < max_:
      raise AssertionError(
          f"The argument must be in ({min_}, {max_}), got {x}.")

