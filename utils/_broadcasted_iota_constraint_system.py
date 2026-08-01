
def _broadcasted_iota_constraint_system(
    ctx: DerivationContext,
    op: mgpu.BroadcastedIotaOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  value = ValueSite(op, VariableType.RESULT, 0)
  var = cs.Variable(value)
  constraints = [cs.NotOfType(var, fa.WGSplatFragLayout)]
  return cs.ConstraintSystem(constraints=constraints), {var: [value]}

