
def _async_prefetch_constraint_system(
    ctx: DerivationContext,
    op: mgpu.AsyncPrefetchOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  value_sites, assignments = _vector_value_sites_and_assignments_for_async_ops(op)
  return cs.ConstraintSystem(assignments), value_sites

