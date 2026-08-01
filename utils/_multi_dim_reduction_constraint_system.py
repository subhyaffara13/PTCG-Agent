
def _multi_dim_reduction_constraint_system(
    ctx: DerivationContext,
    op: vector.MultiDimReductionOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  source = ValueSite(op, VariableType.OPERAND, 0)
  acc = ValueSite(op, VariableType.OPERAND, 1)
  out = ValueSite(op, VariableType.RESULT, 0)
  source_variable = cs.Variable(source)
  out_variable = cs.Variable(out)
  constraints = [
      cs.NotOfType(source_variable, fa.WGStridedFragLayout),
      cs.Equals(
          out_variable,
          cs.Reduce(
              source_variable, tuple(op.reduction_dims), rank=len(source.shape)
          ),
      ),
  ]
  return (
      cs.ConstraintSystem(constraints=constraints),
      {source_variable: [source], out_variable: [acc, out]},
  )

