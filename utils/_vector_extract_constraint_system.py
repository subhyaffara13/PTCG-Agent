
def _vector_extract_constraint_system(
    ctx: DerivationContext, op: vector.ExtractOp
) -> tuple[cs.ConstraintSystem, ValueSitesForVariable]:
  del ctx
  operand = cs.Variable(ValueSite(op, VariableType.OPERAND, 0))
  if not isinstance(op.result.type, ir.VectorType):  # scalar result
    layout = fa.WGSplatFragLayout(tuple(op.source.type.shape))
    # We only support indexing for splat layout.
    assignments: dict[cs.Variable, cs.Constant] = {
        operand: cs.RegisterLayout(layout)
    }
    return cs.ConstraintSystem(assignments), {operand: [operand.key]}

  if op.dynamic_position:
    raise NotImplementedError("Only slicing with static indices allowed.")
  result = cs.Variable(ValueSite(op, VariableType.RESULT, 0))
  constraints = [
      cs.Equals(operand, result),
      cs.Divides(operand, tuple(op.source.type.shape)),
      cs.Divides(result, tuple(op.result.type.shape)),
      # TODO(allanrenucci): Remove once vectors with splat and strided layouts
      # can be sliced.
      cs.NotOfType(result, fa.WGSplatFragLayout),
      cs.NotOfType(result, fa.WGStridedFragLayout),
  ]
  return (
      cs.ConstraintSystem(constraints=constraints),
      {operand: [operand.key], result: [result.key]},
  )

