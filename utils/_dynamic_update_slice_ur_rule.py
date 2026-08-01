
def _dynamic_update_slice_ur_rule(operand, update, *start_indices):
  return _dus_unreduced_rule(operand, update), _dus_reduced_rule(operand, update)

