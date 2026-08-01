
def _constant_constraint_system(
    ctx: DerivationContext,
    constant_op: arith.ConstantOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  value = constant_op.value
  result = ValueSite(constant_op, VariableType.RESULT, 0)
  variable = cs.Variable(result)
  shape = tuple(ir.ShapedType(constant_op.result.type).shape)
  if (
      isinstance(value, ir.DenseElementsAttr)
      and ir.DenseElementsAttr(value).is_splat
  ):
    layout = fa.WGSplatFragLayout(shape=shape)
    system = cs.ConstraintSystem(
        assignments={variable: cs.RegisterLayout(layout)}
    )
  else:
    constant_is_not_splat = cs.NotOfType(variable, fa.WGSplatFragLayout)
    system = cs.ConstraintSystem(constraints=[constant_is_not_splat])

  return system, {variable: [result]}

