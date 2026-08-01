
def _vector_broadcast_constraint_system(
    ctx: DerivationContext,
    op: vector.BroadcastOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  # This is not expected to be necessary at the moment. We should be using
  # mgpu.BroadcastInDimOp instead when dealing with broadcasting vectors.
  if isinstance(op.source.type, ir.ShapedType):
    raise NotImplementedError("Only vector broadcasts from scalars are supported.")
  out_variable = cs.Variable(ValueSite(op, VariableType.RESULT, 0))
  layout = cs.RegisterLayout(fa.WGSplatFragLayout(tuple(op.result.type.shape)))
  return (
      cs.ConstraintSystem(assignments={out_variable: layout}),
      {out_variable: [out_variable.key]},
  )

