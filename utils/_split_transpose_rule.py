
def _split_transpose_rule(cotangents, operand, *, sizes, axis):
  assert ad.is_undefined_primal(operand)
  if all(type(t) is ad_util.Zero for t in cotangents):
    return [ad_util.Zero(operand.aval)]
  cotangents = [ct.instantiate() if type(ct) is ad_util.Zero else ct
                for ct in cotangents]
  return [concatenate(cotangents, dimension=axis)]

