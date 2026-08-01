
def rng_uniform(a, b, shape):
  """Stateful PRNG generator. Experimental and its use is discouraged.

  Returns uniformly distributed random numbers in the range [a, b). If
  b <= a, then the result is undefined, and different implementations may
  return different results.

  You should use jax.random for most purposes; this function exists only for
  niche use cases with special performance requirements.

  This API may be removed at any time.
  """
  a, b = core.auto_insert_reshard(a, b)
  return rng_uniform_p.bind(a, b, shape=tuple(shape))

