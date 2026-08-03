from typing import Any

def _deepcopy(self: Array, memo: Any) -> Array:
  del memo  # unused
  return self.copy()

