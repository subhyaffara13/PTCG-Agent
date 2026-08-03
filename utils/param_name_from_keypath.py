from typing import Any, Tuple

def param_name_from_keypath(keypath: Tuple[Any, ...]) -> str:
  """Returns the parameter name for a keypath."""
  return '.'.join(str_keypath(keypath))

