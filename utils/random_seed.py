
def random_seed(seeds: int | typing.ArrayLike, impl: PRNGImpl) -> PRNGKeyArray:
  # Avoid overflow error in X32 mode by first converting ints to int64.
  # This breaks JIT invariance for large ints, but supports the common
  # use-case of instantiating with Python hashes in X32 mode.
  if isinstance(seeds, int):
    seeds_arr = jnp.asarray(np.int64(seeds))
  else:
    seeds_arr = jnp.asarray(seeds)
  if config.random_seed_offset.value:
    seeds_arr += config.random_seed_offset.value
  return random_seed_p.bind(seeds_arr, impl=impl)

