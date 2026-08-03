from typing import Any, Tuple

def str_keypath(keypath: Tuple[Any, ...]) -> Tuple[str, ...]:
  """Returns the parameter name for a keypath."""
  return tuple([str(get_key_name(k)) for k in keypath])

