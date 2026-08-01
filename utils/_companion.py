
def _companion(a: Array) -> Array:
  first_row = -a[1:] / a[0]
  m = a.shape[0] - 1
  out = jnp.eye(m, m, k=-1, dtype=first_row.dtype)
  return out.at[0].set(first_row)

