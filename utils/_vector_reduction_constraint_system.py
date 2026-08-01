
def _vector_reduction_constraint_system(
    ctx: DerivationContext,
    op: vector.ReductionOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  in_variable = cs.Variable(ValueSite(op, VariableType.OPERAND, 0))
  return cs.ConstraintSystem(), {in_variable: [in_variable.key]}

