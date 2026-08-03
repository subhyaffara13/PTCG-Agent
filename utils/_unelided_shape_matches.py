from typing import Optional, Set, Union

def _unelided_shape_matches(
    actual_shape: Sequence[int],
    expected_shape: Sequence[Optional[Union[int, Set[int]]]]) -> bool:
  """Returns True if `actual_shape` is compatible with `expected_shape`."""
  if len(actual_shape) != len(expected_shape):
    return False
  for actual, expected in zip(actual_shape, expected_shape):
    if expected is None:
      continue
    if isinstance(expected, set):
      if actual not in expected:
        return False
    elif actual != expected:
      return False
  return True

