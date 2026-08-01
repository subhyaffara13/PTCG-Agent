
def shard_prng_key(prng_key):
  """Helper to shard (aka split) a PRNGKey for use with pmap'd functions.

  PRNG keys can be used at train time to drive stochastic modules
  e.g. Dropout. We would like a different PRNG key for each local
  device so that we end up with different random numbers on each one,
  hence we split our PRNG key.

  Args:
    prng_key: JAX PRNGKey
  Returns:
    A new array of PRNGKeys with leading dimension equal to local device count.
  """
  return jax.random.split(prng_key, num=jax.local_device_count())

