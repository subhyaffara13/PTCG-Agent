
def _print_layout_constraint_system(
    ctx: DerivationContext,
    op: mgpu.PrintLayoutOp,
) -> ConstraintSystemDerivationRuleResult:
  value = ValueSite(op, VariableType.OPERAND, 0)
  var = cs.Variable(value) if is_vector(op.value) else ctx.producer_ref(value)
  return cs.ConstraintSystem(), {var: [value]}

