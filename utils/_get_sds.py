
def _get_sds(aval: jax_core.AbstractValue):
  if isinstance(aval, state.AbstractRef):
    if aval.memory_space is not None:
      return aval.memory_space(aval.shape, aval.dtype)
    return _get_sds(aval.inner_aval)
  elif isinstance(aval, jax_core.ShapedArray):
    if isinstance(aval.memory_space, jax_core.MemorySpace):
      return jax_core.ShapeDtypeStruct(
          aval.shape, aval.dtype, manual_axis_type=aval.mat,
          sharding=aval.sharding)
    # memory_space is a pallas memory space which is callable
    return aval.memory_space(aval.shape, aval.dtype)
  else:
    raise ValueError(f"Unsupported abstract value: {aval}")

