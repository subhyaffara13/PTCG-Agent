
def _reduction_op_to_ptx(reduction_op: TMAReductionOp) -> str:
  # convert [s|u]min|max to min|max
  return reduction_op[-3:]

