
def _get_cluster_ref_constraint_system(
    ctx: DerivationContext,
    op: mgpu.GetClusterRefOp,
) -> ConstraintSystemDerivationRuleResult:
  source = ValueSite(op, VariableType.OPERAND, 0)
  var_source_dest = ctx.producer_ref(source)
  dest = ValueSite(op, VariableType.RESULT, 0)
  return cs.ConstraintSystem(), {var_source_dest: [source, dest]}

