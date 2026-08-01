
def _async_store_smem_constraint_system(
    ctx: DerivationContext,
    op: mgpu.AsyncStoreSmemOp,
) -> ConstraintSystemDerivationRuleResult:
  system, value_sites_for_variable = _vector_store_constraint_system(ctx, op)
  var = cs.Variable(ValueSite(op, VariableType.OPERAND, 0))
  extra_constraints = cs.ConstraintSystem(
      constraints=[
          cs.NotOfType(var, fa.WGStridedFragLayout),
          cs.NotOfType(var, fa.WGSplatFragLayout),
      ]
  )
  return system & extra_constraints, value_sites_for_variable

