
def _debug_print_constraint_system(
    ctx: DerivationContext,
    op: mgpu.DebugPrintOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  value = ValueSite(op, VariableType.OPERAND, 0)
  return cs.ConstraintSystem(), {cs.Variable(value): [value]}

