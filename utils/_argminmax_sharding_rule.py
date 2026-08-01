
def _argminmax_sharding_rule(operand, *, axes, index_dtype):
  axis, = axes
  return operand.sharding.update(spec=
      util.tuple_delete(operand.sharding.spec, axis))

