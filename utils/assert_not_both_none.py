from typing import Any

def assert_not_both_none(first: Any, second: Any) -> None:
  """Checks that at least one of the arguments is not `None`.

  Args:
    first: A first object.
    second: A second object.

  Raises:
    AssertionError: If ``(first is None) and (second is None)``.
  """
  if first is None and second is None:
    raise AssertionError(
        "At least one of the arguments must be different from `None`.")

