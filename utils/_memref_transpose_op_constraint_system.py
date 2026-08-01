
def _memref_transpose_op_constraint_system(
    ctx: DerivationContext,
    op: memref.TransposeOp,
) -> ConstraintSystemDerivationRuleResult:
  source = ValueSite(op, VariableType.OPERAND, 0)
  dest = ValueSite(op, VariableType.RESULT, 0)
  source_var = ctx.producer_ref(source)

  dest_var = cs.Variable(dest)

  permutation = tuple(
      ir.AffineDimExpr(e).position for e in op.permutation.value.results
  )
  inv_permutation = tuple(permutation.index(i) for i in range(len(permutation)))

  constraints = [
      cs.Equals(cs.Transpose(source_var, permutation=permutation), dest_var),
      cs.Equals(source_var, cs.Transpose(dest_var, permutation=inv_permutation)),
  ]
  system = cs.ConstraintSystem(constraints=constraints)
  return system, {source_var: [source], dest_var: [dest]}

