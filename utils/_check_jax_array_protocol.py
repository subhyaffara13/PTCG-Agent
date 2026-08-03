from typing import Any

def _check_jax_array_protocol(x: Any) -> Any:
  m = getattr(x, '__jax_array__', None)
  return m() if m is not None else x

