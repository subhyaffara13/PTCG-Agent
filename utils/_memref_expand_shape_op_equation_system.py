
def _memref_expand_shape_op_equation_system(
    ctx: DerivationContext,
    op: memref.ExpandShapeOp,
) -> ConstraintSystemDerivationRuleResult:
  if utils.is_memref_transposed(ir.MemRefType(op.src.type)):
    raise NotImplementedError(
        "Transposed memrefs are not supported in ExpandShapeOp."
    )

  source = ValueSite(op, VariableType.OPERAND, 0)
  source_var = ctx.producer_ref(source)
  dest = ValueSite(op, VariableType.RESULT, 0)
  dest_var = cs.Variable(dest)

  reverse_tiling_multiple = []
  for dim, idx in zip(
      reversed(op.static_output_shape), reversed(op.reassociation)
  ):
    # pyrefly: ignore[bad-argument-type]
    if ir.ShapedType.is_dynamic_size(dim) or len(idx) > 1:
      # For simplicity, we only support tiling non-expanded static dimensions.
      # These limitations could be lifted later if needed.
      break
    reverse_tiling_multiple.append(dim)

  constraints = [
      cs.Divides(source_var, tuple(reversed(reverse_tiling_multiple))),
      cs.Equals(source_var, dest_var),
  ]
  return cs.ConstraintSystem(constraints=constraints), {
      source_var: [source],
      dest_var: [dest],
  }

