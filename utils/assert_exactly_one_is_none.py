from typing import Any

def assert_exactly_one_is_none(first: Any, second: Any) -> None:
  """Checks that one and only one of the arguments is `None`.

  Args:
    first: A first object.
    second: A second object.

  Raises:
    AssertionError: If ``(first is None) xor (second is None)`` is `False`.
  """
  if (first is None) == (second is None):
    raise AssertionError(f"One and exactly one of inputs should be `None`, "
                         f"got {first} and {second}.")

