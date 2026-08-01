
def get_uninitialized_value(
    dtype, uninitialized_memory: Literal["nan", "zero"]
):
  if uninitialized_memory == "nan":
    if jnp.issubdtype(dtype, jnp.floating):
      return np.nan
    elif jnp.issubdtype(dtype, jnp.integer):
      return jnp.iinfo(dtype).max
    elif jnp.issubdtype(dtype, jnp.bool):
      return True
  if uninitialized_memory == "zero":
    return 0
  raise NotImplementedError(uninitialized_memory + " + " + str(dtype))

