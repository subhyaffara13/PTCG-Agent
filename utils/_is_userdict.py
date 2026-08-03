from typing import Any

def _is_userdict(obj: Any, *, force: bool = False) -> bool:
  """Returns `True` if the object is a `collections.UserDict`."""
  if not isinstance(obj, collections.UserDict):
    return False
  if force:  # Force pretty-print even if custom `__repr__`
    return True
  if type(obj).__repr__ == collections.UserDict.__repr__:  # Default repr
    return True
  return False  # Custom repr, do not pretty-print

