
def _gamma(key, a, shape, dtype, log_space=False) -> Array:
  if shape is None:
    shape = np.shape(a)
  else:
    _check_shape("gamma", shape, np.shape(a))

  a = lax.convert_element_type(a, dtype)
  if np.shape(a) != shape:
    a = jnp.broadcast_to(a, shape)
  key, (a,) = random_insert_pvary('gamma', key, a)
  return random_gamma_p.bind(key, a, log_space=log_space)

