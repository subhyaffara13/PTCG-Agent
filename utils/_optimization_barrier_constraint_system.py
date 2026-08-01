
def _optimization_barrier_constraint_system(
    ctx: DerivationContext,
    op: mgpu.OptimizationBarrierOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  value_sites_for_variable: ValueSitesForVariable = {}

  for i, operand in enumerate(op.operands):
    if not is_vector(operand):
      continue
    variable = cs.Variable(ValueSite(op, VariableType.OPERAND, i))
    value_sites_for_variable[variable] = [
        ValueSite(op, VariableType.OPERAND, i),
        ValueSite(op, VariableType.RESULT, i)
    ]

  return cs.ConstraintSystem(), value_sites_for_variable

