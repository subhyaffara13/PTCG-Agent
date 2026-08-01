
def _memref_collapse_shape_op_constraint_system(
    ctx: DerivationContext,
    op: memref.CollapseShapeOp,
) -> ConstraintSystemDerivationRuleResult:
  reassociation = tuple(len(ir.ArrayAttr(idx)) for idx in op.reassociation)
  # This should only occur when going from a (1, ...) shape to an empty shape.
  # We can handle it if needed, but right now `CollapseShape` will not deal with
  # this case.
  if not reassociation:
    raise NotImplementedError(
        "CollapseShapeOp with empty reassociation is not supported."
    )

  source = ValueSite(op, VariableType.OPERAND, 0)
  source_var = ctx.producer_ref(source)
  dest = ValueSite(op, VariableType.RESULT, 0)
  dest_var = cs.Variable(dest)

  strides, _ = ir.MemRefType(source.value.type).get_strides_and_offset()
  # In this case, we'd need additional checks to produce a correct constraint.
  if strides != utils.get_contiguous_strides(source.shape):
    raise NotImplementedError(
        "CollapseShapeOp with non-contiguous strides is not supported."
    )

  # TODO(bchetioui): We could generate an inverse expression `ExpandShape` in
  # order to allow inferring layouts bidirectionally. This would allow removing
  # transforms from some kernels' BlockSpecs, but is not necessary at this time.
  collapse_expr = cs.CollapseShape(source_var, source.shape, reassociation)
  return cs.ConstraintSystem(constraints=[cs.Equals(dest_var, collapse_expr)]), {
      source_var: [source],
      dest_var: [dest],
  }

