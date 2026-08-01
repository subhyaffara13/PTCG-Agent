
def _key(ctor_name: str, seed: int | ArrayLike,
         impl_spec: PRNGSpecDesc | None) -> Array:
  impl = resolve_prng_impl(impl_spec)
  if hasattr(seed, 'dtype') and dtypes.issubdtype(seed.dtype, dtypes.prng_key):
    raise TypeError(
        f"{ctor_name} accepts a scalar seed, but was given a PRNG key.")
  if np.ndim(seed):
    raise TypeError(
        f"{ctor_name} accepts a scalar seed, but was given an array of "
        f"shape {np.shape(seed)} != (). Use jax.vmap for batching")
  return prng.random_seed(seed, impl=impl)

