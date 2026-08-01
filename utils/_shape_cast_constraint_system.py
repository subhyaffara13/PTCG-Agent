
def _shape_cast_constraint_system(
    ctx: DerivationContext, op: vector.ShapeCastOp
) -> ConstraintSystemDerivationRuleResult:
  del ctx
  in_shape = tuple(cast(ir.ShapedType, op.source.type).shape)
  out_shape = tuple(cast(ir.ShapedType, op.result.type).shape)

  in_variable = cs.Variable(ValueSite(op, VariableType.OPERAND, 0))
  out_variable = cs.Variable(ValueSite(op, VariableType.RESULT, 0))

  # Here, we are in a case where we are stating
  #
  #   out_variable = reshape(in_variable, in_shape, out_shape).
  #
  # Thanks to the symmetric property of reshape, we can also issue a constraint
  # in the other direction, i.e.
  #
  #   in_variable = reshape(out_variable, out_shape, in_shape)
  #
  # in order to be able to figure out an assignment for `in_variable`. if we
  # happen to know `out_variable`. If we only issue the first constraint, then
  # we will not be able to figure out an assignment for `in_variable` if we
  # only know `out_variable`, even though their relationship is fully
  # determined.
  in_to_out = cs.Reshape(
      in_variable, source_shape=in_shape, target_shape=out_shape
  )
  out_to_in = cs.Reshape(
      out_variable, source_shape=out_shape, target_shape=in_shape
  )

  return (
      cs.ConstraintSystem(
          constraints=[
              cs.Equals(lhs=out_variable, rhs=in_to_out),
              cs.Equals(lhs=in_variable, rhs=out_to_in),
          ],
      ),
      {in_variable: [in_variable.key], out_variable: [out_variable.key]},
  )

