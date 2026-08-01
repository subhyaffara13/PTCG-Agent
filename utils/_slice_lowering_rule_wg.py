
def _slice_lowering_rule_wg(
    ctx: LoweringRuleContext, x, limit_indices, start_indices, strides
):
  del limit_indices
  assert isinstance(x.type, ir.VectorType)
  if strides is not None:
    raise NotImplementedError("Strides are not supported.")
  out_ty = ir.VectorType.get(
      ctx.avals_out[0].shape, ir.VectorType(x.type).element_type
  )
  sizes = ctx.avals_out[0].shape
  strides = [1] * len(start_indices)
  return vector_dialect.extract_strided_slice(
      out_ty, x, start_indices, sizes, strides
  )

