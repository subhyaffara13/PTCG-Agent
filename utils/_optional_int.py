from typing import Any, Optional

def _optional_int(x: Any) -> Optional[int]:
  if x is None:
    return None
  try:
    i = int(x)
    if x == i:
      return i
  except ValueError:
    pass
  raise TypeError(f'object cannot be interpreted as a python int: {repr(x)}')

