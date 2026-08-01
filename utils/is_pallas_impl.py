
def is_pallas_impl(impl: jax_prng.PRNGImpl) -> bool:
  """Returns True if the PRNGImpl is a Pallas-specific implementation."""
  return impl == tpu_key_impl or impl == tpu_internal_stateful_impl

