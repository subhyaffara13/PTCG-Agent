import sys
from typing import Any

def _is_immutabledict(obj: Any, *, force: bool = False) -> bool:
  """Returns `True` if the object is an `immutabledict`."""
  if 'immutabledict' not in sys.modules:
    return False
  import immutabledict  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error

  if not isinstance(obj, immutabledict.immutabledict):
    return False
  if force:  # Force pretty-print even if custom `__repr__`
    return True
  if type(obj).__repr__ == immutabledict.immutabledict.__repr__:  # Default repr
    return True
  return False  # Custom repr, do not pretty-print

