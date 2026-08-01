
def _tmem_dealloc_constraint_system(
    ctx: DerivationContext,
    op: mgpu.TmemDeallocOp,
) -> ConstraintSystemDerivationRuleResult:
  operand = ValueSite(op, VariableType.OPERAND, 0)
  variable = ctx.producer_ref(operand)
  return cs.ConstraintSystem(), {variable: [operand]}

