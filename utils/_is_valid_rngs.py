
def _is_valid_rngs(rngs: PRNGKey | RNGSequences):
  if not isinstance(rngs, (FrozenDict, dict)):
    return False
  for key, val in rngs.items():
    if not isinstance(key, str):
      return False
    if not _is_valid_rng(val):
      return False
  return True

