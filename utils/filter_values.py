from typing import Any

def filter_values(
    existing: 'PartsOf[T]',
    value_keys: set[tuple[Any, ...]],
) -> 'PartsOf[T]':
  """Makes a new PartsOf from existing with only the values with given keys."""
  # pylint:disable=protected-access
  result = PartsOf.empty(existing._get_template())
  result._present = {
      k: v for k, v in existing._present.items() if k in value_keys
  }
  # pylint:enable=protected-access
  return result

