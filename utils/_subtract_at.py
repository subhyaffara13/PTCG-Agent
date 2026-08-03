from typing import Any

def _subtract_at(a: Array, indices: Any, b: ArrayLike) -> Array:
  """Implementation of jnp.subtract.at."""
  return a.at[indices].subtract(b)

