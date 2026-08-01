
def _insert_strided_slice_constraint_system(
    ctx: DerivationContext, op: vector.InsertStridedSliceOp
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  if any(ir.IntegerAttr(s).value != 1 for s in op.strides):
    raise NotImplementedError("`strides` must contain only 1s.")
  src = cs.Variable(ValueSite(op, VariableType.OPERAND, 0))
  dst = cs.Variable(ValueSite(op, VariableType.OPERAND, 1))
  result = cs.Variable(ValueSite(op, VariableType.RESULT, 0))
  offsets = tuple(ir.IntegerAttr(o).value for o in op.offsets)
  constraints = [
      cs.Divides(dst, offsets),
      cs.Equals(dst, src),
      cs.Equals(dst, result),
      cs.Equals(src, result),
      # TODO(allanrenucci): Remove once vectors with splat and strided layouts
      # can be sliced.
      cs.NotOfType(dst, fa.WGSplatFragLayout),
      cs.NotOfType(dst, fa.WGStridedFragLayout),
  ]
  return (
      cs.ConstraintSystem(constraints=constraints),
      {src: [src.key], dst: [dst.key], result: [result.key]},
  )

