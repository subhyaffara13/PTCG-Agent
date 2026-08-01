
def _memref_cast_op_constraint_system(
    ctx: DerivationContext,
    op: memref.CastOp,
) -> ConstraintSystemDerivationRuleResult:
  source = ValueSite(op, VariableType.OPERAND, 0)
  var_source_dest = ctx.producer_ref(source)
  dest = ValueSite(op, VariableType.RESULT, 0)
  return cs.ConstraintSystem(), {var_source_dest: [source, dest]}

