
def _layout_cast_constraint_system(
    ctx: DerivationContext,
    op: mgpu.LayoutCastOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  operand = ValueSite(op, VariableType.OPERAND, 0)
  operand_var = cs.Variable(operand)
  result = ValueSite(op, VariableType.RESULT, 0)
  result_var = cs.Variable(result)
  out_layout = cs.RegisterLayout(layouts_lib.from_layout_attr(op.new_layout))
  if not cs.is_valid_assignment(result_var, out_layout):
    raise ValueError(
        f"Cannot cast to layout {out_layout.value}: the layout is not"
        f"compatible with the operand shape {operand.shape} in {op}."
    )
  bitwidth = utils.bitwidth(op.x.type.element_type)
  return (
      cs.ConstraintSystem(
          assignments={result_var: out_layout},
          constraints=[
              cs.Relayout(operand_var, result_var, bitwidth, strict=False),
          ],
      ),
      {operand_var: [operand], result_var: [result]},
  )

