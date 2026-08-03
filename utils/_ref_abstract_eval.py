from typing import Any

def _ref_abstract_eval(init_aval, *, memory_space: Any, kind: Any):
  from jax._src.state.types import AbstractRef  # pyrefly: ignore[missing-import]
  # If no memory space is specified, use the memory space of the initial value
  # but we make sure to reset it to Device because the Ref owns the memory space
  if (memory_space is None
      and isinstance(init_aval, ShapedArray)):
    if init_aval.memory_space is not MemorySpace.Device:
      memory_space = init_aval.memory_space
    init_aval = init_aval.update(memory_space=MemorySpace.Device)
  return (AbstractRef(init_aval, memory_space=memory_space, kind=kind),
          {internal_mutable_array_effect})

