
def _reduce_sharding_rule(*avals, computation, jaxpr, dimensions):
  operand_avals, _ = split_list(avals, [len(avals) // 2])
  return [op.sharding.update(spec=tuple_delete(op.sharding.spec, dimensions))
          for op in operand_avals]

