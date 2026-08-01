
def key_dtype(impl_spec: PRNGSpecDesc | None = None) -> prng.KeyTy:
  """Get the dtype corresponding to a PRNG implementation."""
  return prng.KeyTy(resolve_prng_impl(impl_spec))

