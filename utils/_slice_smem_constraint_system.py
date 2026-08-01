
def _slice_smem_constraint_system(
    ctx: DerivationContext,
    op: mgpu.SliceSMEMOp,
) -> ConstraintSystemDerivationRuleResult:
  result = ValueSite(op, VariableType.RESULT, 0)
  if "alias_id" in op.attributes:
    alias_id = ir.IntegerAttr(op.attributes["alias_id"]).value
    alias_key = _AliasKey(None, op.offset.value, alias_id)
    if (cached_variable := ctx.slice_smem_aliases.get(alias_key)) is not None:
      result_variable = cached_variable
    else:
      result_variable = cs.Variable(result)
      ctx.slice_smem_aliases[alias_key] = result_variable
  else:
    result_variable = cs.Variable(result)
  return cs.ConstraintSystem(), {result_variable: [result]}

