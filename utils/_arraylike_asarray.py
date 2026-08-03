from typing import Any

def _arraylike_asarray(x: Any) -> Array:
  """Convert an array-like object to an array."""
  m = getattr(x, '__jax_array__', None)
  if m is not None:
    x = m()
  return lax.asarray(x)

