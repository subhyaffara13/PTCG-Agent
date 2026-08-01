
def _stack_ur_rule(*operands, **kwargs):
  out_unreduced = _concatenate_unreduced_rule(*operands, **kwargs)
  out_reduced = _concatenate_reduced_rule(*operands, **kwargs)
  return out_unreduced, out_reduced

