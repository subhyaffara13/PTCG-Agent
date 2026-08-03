from typing import Any

def _uses_legacy_empty_namedtuple_restore(value: Any) -> bool:
  """Returns whether legacy metadata restore represents `value` as `None`."""
  return tree_utils.isinstance_of_namedtuple(value) and not value

