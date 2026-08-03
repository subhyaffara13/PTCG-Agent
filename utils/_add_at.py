from typing import Any

def _add_at(a: Array, indices: Any, b: ArrayLike) -> Array:
  """Implementation of jnp.add.at."""
  if a.dtype == bool:
    a = a.astype('int32')
    b = lax.convert_element_type(b, bool).astype('int32')
    return a.at[indices].add(b).astype(bool)
  return a.at[indices].add(b)

