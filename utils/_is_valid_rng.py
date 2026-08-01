
def _is_valid_rng(rng: Array):
  """Checks whether rng is a valid JAX PRNGKey, also handling custom prngs."""
  # Allow for user-provided LazyRng - useful for compatibility when refactoring.
  if isinstance(rng, LazyRng):
    return True

  # This check is valid for either new-style or old-style PRNG keys
  if not isinstance(rng, (np.ndarray, jnp.ndarray)):
    return False

  # Handle new-style typed PRNG keys
  if jax.dtypes.issubdtype(rng.dtype, jax.dtypes.prng_key):
    return rng.shape == ()

  # Handle old-style raw PRNG keys
  expected_rng = jax.eval_shape(
    lambda s: jax.random.key_data(jax.random.key(s)), 0
  )
  if (rng.shape, rng.dtype) != (expected_rng.shape, expected_rng.dtype):
    return False
  return True

