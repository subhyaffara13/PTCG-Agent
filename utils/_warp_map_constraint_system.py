
def _warp_map_constraint_system(
    ctx: DerivationContext,
    op: mgpu.WarpMapOp,
) -> ConstraintSystemDerivationRuleResult:
  value_sites_for_variable: ValueSitesForVariable = dict()
  for i, o in enumerate(op.operands):
    if _is_tmem_ref(o) or _is_smem_ref(o):
      operand = ValueSite(op, VariableType.OPERAND, i)
      arg = ValueSite(op, VariableType.ARGUMENT, i, region_index=0)
      var = ctx.producer_ref(operand)
      value_sites_for_variable.setdefault(var, []).extend([operand, arg])
  return cs.ConstraintSystem(), value_sites_for_variable

