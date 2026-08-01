
def key_impl(keys: ArrayLike) -> str | PRNGSpec:
  typed_keys, _ = _check_prng_key("key_impl", keys, allow_batched=True)
  return _key_spec(typed_keys)

