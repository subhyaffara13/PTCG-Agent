
def wrap_pallas_seed(*seeds, impl):
  """Joins scalar into a single PRNG key."""
  impl = jax_random.resolve_prng_impl(impl)
  return join_key_p.bind(*seeds, impl=impl)

