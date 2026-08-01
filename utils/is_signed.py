
def is_signed(dtype: jax.typing.DTypeLike) -> bool | None:
  if jnp.issubdtype(dtype, jnp.bool_):
    return False
  elif jnp.issubdtype(dtype, jnp.integer):
    return jnp.issubdtype(dtype, jnp.signedinteger)
  return None

