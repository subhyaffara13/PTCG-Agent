
def _reduce_op_sharding_rule(operand, *, axes):
  axes = frozenset(axes)
  new_spec = P(*tuple(s for i, s in enumerate(operand.sharding.spec)
                      if i not in axes))
  return operand.sharding.update(spec=new_spec)

