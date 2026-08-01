
def _unstack_transpose_rule(cotangents, operand, *, axis):
  if all(type(ct) is ad_util.Zero for ct in cotangents):
    return [ad_util.Zero(operand.aval)]
  cotangents = [ct.instantiate() if type(ct) is ad_util.Zero else ct
                for ct in cotangents]
  return [stack_p.bind(*cotangents, axis=axis)]

