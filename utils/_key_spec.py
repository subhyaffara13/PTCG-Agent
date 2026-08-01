
def _key_spec(keys: Array) -> str | PRNGSpec:
  impl = _key_impl(keys)
  return impl.name if impl.name in prng.prngs else PRNGSpec(impl)

