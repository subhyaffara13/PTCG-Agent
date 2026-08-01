
def _stack_transpose_rule(ct, *operands, axis):
  if type(ct) is ad_util.Zero:
    return [ad_util.Zero(o.aval) if ad.is_undefined_primal(o) else None
            for o in operands]
  return unstack_p.bind(ct, axis=axis)

