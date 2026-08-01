
def _pl_stateful_seed_func(seed: jnp.int32):
  del seed
  # Unused. Return the correct shape and dtype.
  return jnp.empty((), dtype=jnp.int32)

