
def get_var_pspec(v: variablelib.Variable) -> PartitionSpec | None:
  """Given an `nnx.Variable`, return its `PartitionSpec`."""
  metadata = v.get_metadata()
  if 'out_sharding' in metadata and metadata['out_sharding']:
    sharding = metadata['out_sharding']
    if core_spmd.get_logical_axis_rules() or 'sharding_rules' in metadata:
      context_rules = core_spmd.get_logical_axis_rules()
      local_rules = metadata.get('sharding_rules', ())
      rules = core_spmd.composite_rules(context_rules, local_rules)
      return PartitionSpec(*core_spmd.from_sharding_rules(sharding, rules))
    return PartitionSpec(*sharding)
  elif hasattr(v, 'shape'):
      return PartitionSpec()
  return None

