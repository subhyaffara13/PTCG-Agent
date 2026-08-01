
def _extract_strided_slice_constraint_system(
    ctx: DerivationContext, op: vector.ExtractStridedSliceOp
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  if any(ir.IntegerAttr(s).value != 1 for s in op.strides):
    raise NotImplementedError("`strides` must contain only 1s.")
  operand = cs.Variable(ValueSite(op, VariableType.OPERAND, 0))
  result = cs.Variable(ValueSite(op, VariableType.RESULT, 0))
  offsets = tuple(ir.IntegerAttr(o).value for o in op.offsets)
  constraints = [
      cs.Divides(operand, offsets),
      cs.Equals(operand, result),
      # TODO(allanrenucci): Remove once vectors with splat and strided layouts
      # can be sliced.
      cs.NotOfType(result, fa.WGSplatFragLayout),
      cs.NotOfType(result, fa.WGStridedFragLayout),
  ]
  return (
      cs.ConstraintSystem(constraints=constraints),
      {operand: [operand.key], result: [result.key]},
  )

