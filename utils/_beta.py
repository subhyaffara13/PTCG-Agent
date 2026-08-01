
def _beta(key, a, b, shape, dtype) -> Array:
  if shape is None:
    shape = lax.broadcast_shapes(np.shape(a), np.shape(b))
  else:
    _check_shape("beta", shape, np.shape(a), np.shape(b))

  key, (a, b) = random_insert_pvary("jax.random.beta", key, a, b)

  a = lax.convert_element_type(a, dtype)
  b = lax.convert_element_type(b, dtype)
  key_a, key_b = _split(key)
  a = jnp.broadcast_to(a, shape)
  b = jnp.broadcast_to(b, shape)
  log_gamma_a = loggamma(key_a, a, shape, dtype)
  log_gamma_b = loggamma(key_b, b, shape, dtype)
  # Compute gamma_a / (gamma_a + gamma_b) without losing precision.
  log_max = lax.max(log_gamma_a, log_gamma_b)
  gamma_a_scaled = jnp.exp(log_gamma_a - log_max)
  gamma_b_scaled = jnp.exp(log_gamma_b - log_max)
  return gamma_a_scaled / (gamma_a_scaled + gamma_b_scaled)

