
def _remove_memory_space_abstract_eval(x):
  if (isinstance(x, jax_core.ShapedArray) and
      not isinstance(x.memory_space, jax_core.MemorySpace)):
    if (x.memory_space is None or x.memory_space is pallas_core.MemorySpace.ANY
        or x.memory_space is mosaic_core.MemorySpace.HBM):
      return jax_core.ShapedArray(x.shape, x.dtype)
    raise NotImplementedError(f'Unsupported memory space: {x.memory_space}')
  return x

