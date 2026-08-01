
def normalised_by_sum(v, axis=0):
  """Divides each element of `v` along `axis` by the sum of `v` along `axis`."""
  s = jnp.sum(v, axis=axis, keepdims=True)
  safe_s = jnp.where(s == 0, 1.0, s)
  out = v / safe_s
  return jnp.where(s == 0, 1.0 / v.shape[axis], out)

