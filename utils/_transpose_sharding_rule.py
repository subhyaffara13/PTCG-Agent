
def _transpose_sharding_rule(operand, *, permutation):
  o_spec = operand.sharding.spec
  new_spec = [o_spec.partitions[old_idx] for old_idx in permutation]
  return operand.sharding.update(spec=o_spec.update(partitions=new_spec))

