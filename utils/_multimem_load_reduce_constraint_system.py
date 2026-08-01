
def _multimem_load_reduce_constraint_system(
    _: DerivationContext,
    op: mgpu.MultimemLoadReduceOp,
) -> ConstraintSystemDerivationRuleResult:
  dest = ValueSite(op, VariableType.RESULT, 0)
  dest_var = cs.Variable(dest)
  system = cs.ConstraintSystem(
      constraints=[cs.NotOfType(dest_var, fa.WGSplatFragLayout)]
  )
  return system, {dest_var: [dest]}

