from typing import Any

def is_multi_device_array(value: Any) -> bool:
  """Instruct Orbax to save this array with Tensorstore instead of msgpack."""
  if isinstance(value, jax.Array):
    return not value.is_fully_replicated
  return False

