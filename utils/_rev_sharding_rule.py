
def _rev_sharding_rule(operand, *, dimensions):
  # TODO(yashkatariya): Will lead to data movement. Maybe just error out and
  # require the operand to be unsharded?
  return operand.sharding

