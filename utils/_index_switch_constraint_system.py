
def _index_switch_constraint_system(
    ctx: DerivationContext,
    op: scf.IndexSwitchOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  value_sites_for_variable: ValueSitesForVariable = {
      cs.Variable(o): [o] for o in vector_value_sites(op)
  }
  for region in op.regions:
    [block] = region.blocks
    yield_op = _terminator(block, scf.YieldOp)
    for var in value_sites_for_variable.keys():
      assert var.key.type == VariableType.RESULT
      yield_operand = ValueSite(yield_op, VariableType.OPERAND, var.key.index)
      value_sites_for_variable[var].append(yield_operand)

  return cs.ConstraintSystem(), value_sites_for_variable

