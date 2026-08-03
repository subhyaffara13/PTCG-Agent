from typing import Any

def is_supported_leaf(x: Any) -> bool:
  """Returns True if the given object is a supported concrete Leaf."""
  return isinstance(x, types.Leaf)

