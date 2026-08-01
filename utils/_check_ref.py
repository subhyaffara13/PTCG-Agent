
def _check_ref(
    aval: object, name: str, memory_space: gpu_core.MemorySpace
) -> None:
  if not isinstance(aval, state_types.AbstractRef):
    raise TypeError(f"{name} must be a reference, got {aval}")
  aval_memory_space = getattr(aval, "memory_space", None)
  if (
      aval_memory_space is None
      or aval_memory_space is pallas_core.MemorySpace.DEFAULT
  ):
    aval_memory_space = gpu_core.GMEM
  if aval_memory_space is not memory_space:
    raise ValueError(
        f"{name} must be a {memory_space.name.upper()} reference, got {aval}"
    )

