
def _pointwise_op_constraint_system(
    ctx: DerivationContext,
    op: ir.OpView,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  all_value_sites = vector_value_sites(op)
  variable = cs.Variable(all_value_sites[-1])
  return cs.ConstraintSystem(), {variable: all_value_sites}

