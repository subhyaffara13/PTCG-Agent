
def _is_replicated_sdy(attr: ir.Attribute) -> bool:
  if isinstance(attr, sdy.TensorShardingAttr):
    return all(len(cast(sdy.DimensionShardingAttr, dim).axes) == 0
               for dim in attr.dimension_shardings)
  if isinstance(attr, sdy.TensorShardingPerValueAttr):
    return all(_is_replicated_sdy(s) for s in attr.shardings)
  return False

