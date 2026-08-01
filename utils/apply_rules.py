
def apply_rules(sharding, sharding_rules):
  """Rename the axes of a sharding specification (which can include `PartitionSpec`, `NamedSharding` or `Format` objects)."""
  if get_logical_axis_rules() or sharding_rules:
    context_rules = get_logical_axis_rules()
    rules = {alias: on_mesh for (alias, on_mesh) in composite_rules(context_rules, sharding_rules)}
  else:
    rules = {}
  return map_sharding(lambda a: rules.get(a, a), sharding)

