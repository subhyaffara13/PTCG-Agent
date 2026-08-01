
def _for_constraint_system(
    ctx: DerivationContext,
    op: scf.ForOp,
) -> ConstraintSystemDerivationRuleResult:
  [block] = op.region.blocks
  yield_op = _terminator(block, scf.YieldOp)
  value_sites_for_variable: ValueSitesForVariable = {}

  # Account for the lower bound, upper bound, and step of the loop, which appear
  # in the operands but not in the results.
  num_leading_args = 3
  for index, o in enumerate(op.operands):
    if not is_vector(o) and not _is_smem_ref(o):
      continue
    result_index = index - num_leading_args
    arg_index = index - num_leading_args + 1  # Account for the induction var.
    operand = ValueSite(op, VariableType.OPERAND, index)
    arg = ValueSite(op, VariableType.ARGUMENT, arg_index, region_index=0)
    result = ValueSite(op, VariableType.RESULT, result_index)
    yield_operand = ValueSite(
        yield_op, VariableType.OPERAND, result_index
    )
    var = cs.Variable(operand) if is_vector(o) else ctx.producer_ref(operand)
    value_sites_for_variable[var] = [operand, arg, result, yield_operand]

  return cs.ConstraintSystem(), value_sites_for_variable

