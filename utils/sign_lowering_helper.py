
def sign_lowering_helper(x):
  if jnp.issubdtype(x.dtype, jnp.unsignedinteger):
    return (x != 0).astype(x.dtype)

  if jnp.issubdtype(x.dtype, jnp.integer):
    return (x > 0).astype(x.dtype) - (x < 0).astype(x.dtype)

  if jnp.issubdtype(x.dtype, jnp.floating):
    out = (x > 0.).astype(x.dtype) - (x < 0.).astype(x.dtype)
    return jnp.where(jnp.isnan(x), jnp.nan, out)

  raise NotImplementedError(f"sign_lowering_helper not implemented for {x.dtype}")

