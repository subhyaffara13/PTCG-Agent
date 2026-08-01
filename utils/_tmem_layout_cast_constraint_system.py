
def _tmem_layout_cast_constraint_system(
    ctx: DerivationContext,
    op: mgpu.TmemLayoutCastOp,
) -> ConstraintSystemDerivationRuleResult:
  operand = ValueSite(op, VariableType.OPERAND, 0)
  variable = ctx.producer_ref(operand)
  result = ValueSite(op, VariableType.RESULT, 0)
  tmem_layout = cs.TMEMLayout(_tmem_layout_from_layout_attr(op.new_layout))
  if not cs.is_valid_assignment(variable, tmem_layout):
    raise ValueError(
        f"Cannot cast to TMEM layout {tmem_layout.value} in {op}: the layout is"
        f" not compatible with the operand shape {operand.shape}."
    )
  return (
      cs.ConstraintSystem(assignments={variable: tmem_layout}),
      {variable: [operand, result]},
  )

