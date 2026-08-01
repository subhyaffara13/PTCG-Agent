
def unwrap_pallas_seed(seed):
  """Splits a PRNG key into it's scalar components."""
  return split_key_p.bind(seed)

