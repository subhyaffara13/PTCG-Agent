
def _memref_subview_constraint_system(
    ctx: DerivationContext,
    op: memref.SubViewOp,
) -> ConstraintSystemDerivationRuleResult:
  source = ValueSite(op, VariableType.OPERAND, 0)
  source_var = ctx.producer_ref(source)
  result = ValueSite(op, VariableType.RESULT, 0)
  result_var = cs.Variable(result)

  if any(s != 1 for s in op.static_strides):
    raise NotImplementedError(
        f"Only unit strides are supported but got {op.static_strides}."
    )

  # Collect all the constraints from all dimensions.
  tiling_multiple = []
  dynamic_offset_index = 0
  for i, size in enumerate(op.static_sizes):
    offset = op.static_offsets[i]
    if offset == ir.ShapedType.get_dynamic_size():
      offset = op.offsets[dynamic_offset_index]
      dynamic_offset_index += 1

    # Drop all dimensions up to and including the last dynamic size. Dynamic
    # sizes are not supported yet.
    #
    # Supporting dynamic sizes here can be done analogously to how dynamic
    # offsets are supported. The reason we don't support dynamic sizes now is
    # because the lowering does not yet support them.
    if ir.ShapedType.is_dynamic_size(size):
      tiling_multiple = []
    else:
      src_type = ir.MemRefType(op.source.type)
      divisibility_constraint = math.gcd(size, src_type.shape[i])
      if isinstance(offset, int):
        divisibility_constraint = math.gcd(divisibility_constraint, offset)
      else:
        divisibility_constraint = dynamic_gcd(divisibility_constraint, offset)
      tiling_multiple.append(divisibility_constraint)

  constraints = [
      cs.Divides(source_var, tuple(tiling_multiple)),
      cs.Equals(source_var, result_var),
  ]
  system = cs.ConstraintSystem(constraints=constraints)
  return system, {source_var: [source], result_var: [result]}

