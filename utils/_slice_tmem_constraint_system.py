
def _slice_tmem_constraint_system(
    ctx: DerivationContext,
    op: mgpu.SliceTmemOp,
) -> ConstraintSystemDerivationRuleResult:
  operand = ValueSite(op, VariableType.OPERAND, 0)
  operand_variable = ctx.producer_ref(operand)
  result = ValueSite(op, VariableType.RESULT, 0)
  # TODO(bchetioui): enforce that the parent is a TmemAllocOp.
  if "alias_id" in op.attributes:
    alias_id = ir.IntegerAttr(op.attributes["alias_id"]).value
    alias_key = _AliasKey(None, op.offset.value, alias_id)
    if (cached_variable := ctx.slice_tmem_aliases.get(alias_key)) is not None:
      result_variable = cached_variable
    else:
      result_variable = cs.Variable(result)
      ctx.slice_tmem_aliases[alias_key] = result_variable
  else:
    result_variable = cs.Variable(result)
  return (
      cs.ConstraintSystem(),
      {operand_variable: [operand], result_variable: [result]},
  )

