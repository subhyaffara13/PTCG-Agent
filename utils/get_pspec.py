
def get_pspec(sharding, sharding_rules = None) -> PartitionSpec:
  """Given an `nnx.Variable`, return its `PartitionSpec`."""
  return apply_rules(sharding, sharding_rules)   # type: ignore

