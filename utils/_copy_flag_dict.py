import copy
from typing import Any

def _copy_flag_dict(flag: flags.Flag) -> dict[str, Any]:
  """Returns a copy of the flag object's ``__dict__``.

  It's mostly a shallow copy of the ``__dict__``, except it also does a shallow
  copy of the validator list.

  Args:
    flag: flags.Flag, the flag to copy.

  Returns:
    A copy of the flag object's ``__dict__``.
  """
  copy = flag.__dict__.copy()
  copy['_value'] = flag.value  # Ensure correct restore for C++ flags.
  copy['validators'] = list(flag.validators)
  return copy

