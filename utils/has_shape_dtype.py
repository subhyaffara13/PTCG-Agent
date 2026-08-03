from typing import Any

def has_shape_dtype(x: Any) -> TypeGuard[ShapeDtype]:
  return hasattr(x, 'shape') and hasattr(x, 'dtype')

