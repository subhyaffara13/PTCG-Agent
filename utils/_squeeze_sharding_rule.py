
def _squeeze_sharding_rule(operand, *, dimensions):
  dims_set = set(dimensions)
  new_spec = tuple(s for i, s in enumerate(operand.sharding.spec.partitions)
                   if i not in dims_set)
  return operand.sharding.update(
      spec=operand.sharding.spec.update(partitions=new_spec))

