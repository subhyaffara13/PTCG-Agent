
def _slice_lowering_rule(
    ctx: LoweringRuleContext, x, limit_indices, start_indices, strides
):
  """Lowers a slice to vector dialect."""
  (aval_out,) = ctx.avals_out
  out_type = ctx.aval_to_ir_type(aval_out)
  if strides is None:
    strides = [1] * len(start_indices)
  sizes = np.array(limit_indices) - np.array(start_indices)
  return vector.extract_strided_slice(
      out_type, x, start_indices, sizes, strides
  )


def _slice_lowering_rule(
    ctx: LoweringRuleContext, x, limit_indices, start_indices, strides
):
  if strides is not None:
    raise NotImplementedError("Strides are not supported.")

  return x[tuple(slice(b, e) for b, e in zip(start_indices, limit_indices))]

