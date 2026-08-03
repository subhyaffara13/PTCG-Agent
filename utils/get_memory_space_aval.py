from typing import Any

def get_memory_space_aval(aval: jax_core.AbstractValue) -> Any:
  """Queries the memory space of an array."""
  if (isinstance(aval, jax_core.ShapedArray) and
      not isinstance(aval.memory_space, jax_core.MemorySpace)):
    return aval.memory_space
  if isinstance(aval, state.AbstractRef):
    if aval.memory_space is not None:
      return aval.memory_space
    return get_memory_space_aval(aval.inner_aval)
  return None

