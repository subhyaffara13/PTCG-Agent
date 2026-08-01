
def from_sharding_rules(
    sharding: Sharding, sharding_rules: LogicalRules
) -> Sharding:
  rules = {alias: on_mesh for (alias, on_mesh) in sharding_rules}
  return tuple(
      rules[str(s)] if (s and str(s) in rules) else s for s in sharding
  )

