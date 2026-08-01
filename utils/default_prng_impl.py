
def default_prng_impl():
  """Get the default PRNG implementation.

  The default implementation is determined by ``config.jax_default_prng_impl``,
  which specifies it by name.
  """
  impl_name = config.default_prng_impl.value
  assert impl_name in prng.prngs, impl_name
  return prng.prngs[impl_name]

