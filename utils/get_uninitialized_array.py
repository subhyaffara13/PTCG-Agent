
def get_uninitialized_array(
    shape: tuple[int, ...],
    dtype: jnp.dtype,
    memory_space: mosaic_gpu_core.MemorySpace,
    uninitialized_memory: Literal["nan", "zero"]
) -> jax.Array:
  if memory_space == mosaic_gpu_core.MemorySpace.REGS:
    uninitialized_memory = "zero"
  return interpret_utils.get_uninitialized_array(
      shape, dtype, uninitialized_memory)


def get_uninitialized_array(
    shape, dtype, uninitialized_memory: Literal["nan", "zero"]
):
  return jnp.full(
      shape,
      get_uninitialized_value(dtype, uninitialized_memory),
      dtype,
  )

