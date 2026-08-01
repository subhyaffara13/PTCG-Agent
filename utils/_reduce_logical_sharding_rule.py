
def _reduce_logical_sharding_rule(operand, *, axes):
  return operand.sharding.update(spec=tuple_delete(operand.sharding.spec, axes))

