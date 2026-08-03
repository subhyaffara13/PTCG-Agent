from typing import Any

def is_key_like(x: Any) -> TypeGuard[Key]:
  return hasattr(x, '__hash__') and hasattr(x, '__lt__')

