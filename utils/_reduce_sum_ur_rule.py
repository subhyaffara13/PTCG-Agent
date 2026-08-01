
def _reduce_sum_ur_rule(operand, *, axes, out_sharding):
  out_unreduced = _reduce_sum_unreduced_rule(operand, axes, out_sharding)
  return out_unreduced, getr(operand)

