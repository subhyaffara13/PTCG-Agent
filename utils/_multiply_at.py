from typing import Any

def _multiply_at(a: Array, indices: Any, b: ArrayLike) -> Array:
  """Implementation of jnp.multiply.at."""
  if a.dtype == bool:
    a = a.astype('int32')
    b = lax.convert_element_type(b, bool).astype('int32')
    return a.at[indices].mul(b).astype(bool)
  else:
    return a.at[indices].mul(b)

