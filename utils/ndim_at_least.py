
def ndim_at_least(x, num_dims):
  if not (isinstance(x, jax.Array) or isinstance(x, np.ndarray)):
    x = jnp.asarray(x)
  return x.ndim >= num_dims

