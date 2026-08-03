from typing import Any

def isinstance_of_namedtuple(value: Any) -> bool:
  """Determines if the `value` is a NamedTuple."""
  return isinstance(value, tuple) and hasattr(value, '_fields')

