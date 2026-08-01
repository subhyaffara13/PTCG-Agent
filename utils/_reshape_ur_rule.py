
def _reshape_ur_rule(operand, *, new_sizes, dimensions, sharding):
  out_unreduced = _reshape_unreduced_rule(
      operand, new_sizes=new_sizes, dimensions=dimensions, sharding=sharding)
  out_reduced = _reshape_reduced_rule(
      operand, new_sizes=new_sizes, dimensions=dimensions, sharding=sharding)
  return out_unreduced, out_reduced

