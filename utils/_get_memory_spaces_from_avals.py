
def _get_memory_spaces_from_avals(
    avals: Sequence[jax_core.AbstractValue],
    kernel_type: tpu_core.CoreType | None,
) -> tuple[tpu_custom_call.MemorySpace | None, ...] | None:
  memory_spaces = None
  if any(isinstance(aval, jax_core.ShapedArray)
         and not isinstance(aval.memory_space, jax_core.MemorySpace)
         for aval in avals):
    memory_spaces = tuple(
        _get_memory_space_from_aval(aval, kernel_type=kernel_type)
        for aval in avals)
  return memory_spaces

