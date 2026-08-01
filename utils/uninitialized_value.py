
def uninitialized_value(shape, dtype):
  if jnp.issubdtype(dtype, jnp.floating):
    return jnp.full(shape, jnp.nan, dtype)
  # Note: Currently semaphore is i16[], meaning this case needs to be
  # handled before the general case for integers.
  # TODO(justinfu): Handle semaphores with a custom extended dtype.
  elif jnp.issubdtype(dtype, pallas_core.SEMAPHORE_INTERPRET_DTYPE):
    return jnp.full(shape, 0, dtype)
  elif jnp.issubdtype(dtype, jnp.integer):
    return jnp.full(shape, jnp.iinfo(dtype).min, dtype)
  elif jnp.issubdtype(dtype, jnp.bool):
    return jnp.full(shape, False, dtype)
  elif jnp.issubdtype(dtype, pallas_core.semaphore_dtype):
    return jnp.full(shape, 0, dtype)
  raise NotImplementedError(dtype)

