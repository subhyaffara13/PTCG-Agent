
def _while_constraint_system(
    ctx: DerivationContext,
    op: scf.WhileOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  [before_block] = op.before.blocks
  [after_block] = op.after.blocks
  cond_op = _terminator(before_block, scf.ConditionOp)
  yield_op = _terminator(after_block, scf.YieldOp)

  value_sites_for_variable: ValueSitesForVariable = {}

  for value_site in vector_value_sites(op):
    idx = value_site.index
    match value_site.type:
      case VariableType.OPERAND:
        arg = ValueSite(op, VariableType.ARGUMENT, idx, region_index=0)
        yield_operand = ValueSite(yield_op, VariableType.OPERAND, idx)
        value_sites_for_variable[cs.Variable(value_site)] = [
            value_site,
            arg,
            yield_operand,
        ]
      case VariableType.RESULT:
        # Increment by 1 to account for the conditional.
        cond_operand = ValueSite(cond_op, VariableType.OPERAND, idx + 1)
        arg = ValueSite(op, VariableType.ARGUMENT, idx, region_index=1)
        value_sites_for_variable[cs.Variable(value_site)] = [
            value_site,
            arg,
            cond_operand,
        ]
      case _:
        raise RuntimeError(f"Unexpected value site type: {value_site.type}")

  return cs.ConstraintSystem(), value_sites_for_variable

