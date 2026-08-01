
def _tmem_alloc_constraint_system(
    ctx: DerivationContext,
    op: mgpu.TmemAllocOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  result = ValueSite(op, VariableType.RESULT, 0)
  result_var = cs.Variable(result)
  in_smem = ValueSite(op, VariableType.OPERAND, 0)
  in_smem_var = cs.Variable(in_smem)
  assignments: dict[cs.Variable, cs.Constant] = {
      in_smem_var: cs.SMEMTransforms(None)
  }
  operands_for_variable = {result_var: [result], in_smem_var: [in_smem]}
  return cs.ConstraintSystem(assignments=assignments), operands_for_variable

