
def _wgmma_constraint_system(
    ctx: DerivationContext,
    op: mgpu.WGMMAOp,
) -> ConstraintSystemDerivationRuleResult:
  assignments: dict[cs.Variable, cs.Constant] = {}
  value_sites_for_variable: ValueSitesForVariable = {}

  acc_out = ValueSite(op, VariableType.RESULT, 0)
  acc_in = ValueSite(op, VariableType.OPERAND, 0)
  acc_var = cs.Variable(acc_out)
  acc_layout = cs.RegisterLayout(fa.WGMMA_LAYOUT)
  assignments[acc_var] = acc_layout
  if not cs.is_valid_assignment(acc_var, acc_layout):
    raise ValueError(
        f"Cannot assign layout {acc_layout.value} to the accumulator of a wgmma"
        f" op: the layout is not compatible with the accumulator shape"
        f" {acc_out.shape}."
    )
  value_sites_for_variable[acc_var] = [acc_in, acc_out]

  b = ValueSite(op, VariableType.OPERAND, 2)
  b_var = ctx.producer_ref(b)
  input_bitwidth = utils.bitwidth(op.b.type.element_type)
  b_is_transposed = utils.is_memref_transposed(ir.MemRefType(op.b.type))
  constraints: list[cs.Constraint]
  if b_is_transposed:
    constraints = [cs.IsValidMmaTiling(cs.Transpose(b_var, (1, 0)), input_bitwidth)]
  else:
    constraints = [cs.IsValidMmaTiling(b_var, input_bitwidth)]
  value_sites_for_variable[b_var] = [b]

  a = ValueSite(op, VariableType.OPERAND, 1)
  if _is_smem_ref(op.a):
    a_var = ctx.producer_ref(a)
    # We expect the tiling transform to be physically the same on both sides.
    # However, the constraint system assigns tiling transforms based on the
    # logical shape. In the case the tiled dimensions of exactly one of the
    # operands are transposed, we need to transpose the transform as well.
    a_is_transposed = utils.is_memref_transposed(ir.MemRefType(op.a.type))
    if a_is_transposed != b_is_transposed:
      constraints.append(cs.Equals(lhs=a_var, rhs=cs.Transpose(b_var, (1, 0))))
    else:
      constraints.append(cs.Equals(lhs=a_var, rhs=b_var))
  else:
    a_var = cs.Variable(a)
    if utils.bitwidth(op.a.type.element_type) == 8:
      layout = fa.WGMMA_LAYOUT_8BIT
    else:
      layout = fa.WGMMA_LAYOUT
    layout = cs.RegisterLayout(layout)
    assignments[a_var] = layout
    if not cs.is_valid_assignment(a_var, layout):
      raise ValueError(
          f"Cannot assign layout {layout.value} to the 'a' operand of WGMMAOp: "
          f"the layout is not compatible with the operand shape {a.shape}."
      )

  value_sites_for_variable[a_var] = [a]
  return cs.ConstraintSystem(assignments, constraints), value_sites_for_variable

