
def _tile_transpose_rule(ct, operand, *, reps):
  if type(ct) is ad_util.Zero:
    return [ad_util.Zero(operand.aval)]
  if not isinstance(operand, ad.UndefinedPrimal):
    return [None]  # transpose wrt literal
  out_spec = tuple(s for sp in operand.aval.sharding.spec for s in [None, sp])
  ct_reshaped = reshape(
      ct, tuple(k for pair in zip(reps, operand.aval.shape) for k in pair),
      out_sharding=operand.aval.sharding.update(spec=out_spec))
  axes = tuple(2 * i for i in range(operand.aval.ndim))
  return [reduce_sum(ct_reshaped, axes)]

