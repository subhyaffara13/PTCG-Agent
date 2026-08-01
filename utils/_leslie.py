
def _leslie(f: Array, s: Array) -> Array:
  f, s = promote_dtypes(f, s)
  return jnp.diag(s, k=-1).at[0].set(f)

