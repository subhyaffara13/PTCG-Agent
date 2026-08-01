
def _cluster_launch_control_ops_constraint_system(
    ctx: DerivationContext,
    op: mgpu.TryClusterCancelOp | mgpu.QueryClusterCancelOp,
) -> ConstraintSystemDerivationRuleResult:
  ref = ValueSite(op, VariableType.OPERAND, 0)
  var = ctx.producer_ref(ref)
  assignments: dict[cs.Variable, cs.Constant] = {var: cs.SMEMTransforms(None)}
  return cs.ConstraintSystem(assignments=assignments), {var: [ref]}

