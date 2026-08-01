
def _tcgen05_mma_constraint_system(
    ctx: DerivationContext,
    op: mgpu.TcGen05MMAOp,
) -> ConstraintSystemDerivationRuleResult:
  assignments: dict[cs.Variable, cs.Constant] = {}
  operands_for_variable: ValueSitesForVariable = {}

  # TMEM
  acc = ValueSite(op, VariableType.OPERAND, 0)
  acc_variable = ctx.producer_ref(acc)
  acc_type = ir.ShapedType(op.accumulator.type)
  acc_layout = tcgen05._infer_tmem_layout(
      tuple(acc_type.shape), bool(op.collective), packing=1
  )
  acc_layout = cs.TMEMLayout(acc_layout)
  assignments[acc_variable] = acc_layout
  acc_is_valid = cs.is_valid_assignment(acc_variable, acc_layout)
  if not acc_is_valid:
    raise ValueError(
        f"Cannot assign TMEM layout {acc_layout.value} to the accumulator of"
        f" a tcgen05 MMA op: the layout is not compatible with the accumulator"
        f" shape {acc.shape}."
    )
  operands_for_variable[acc_variable] = [acc]

  element_type_bitwidth = utils.bitwidth(op.b.type.element_type)
  b = ValueSite(op, VariableType.OPERAND, 2)
  b_var = ctx.producer_ref(b)
  operands_for_variable[b_var] = [b]
  b_is_transposed = utils.is_memref_transposed(ir.MemRefType(op.b.type))
  constraints: list[cs.Constraint]
  if b_is_transposed:
    constraints = [cs.IsValidMmaTiling(cs.Transpose(b_var, (1, 0)), element_type_bitwidth)]
  else:
    constraints = [cs.IsValidMmaTiling(b_var, element_type_bitwidth)]

  # SMEM
  M = op.accumulator.type.shape[0]
  if M == 64 and not op.collective.value:
    # We can't split N into groups if we would partition it below the tile size.
    N = op.b.type.shape[1]
    n_lane_groups = 2
    max_swizzle_elems = next(
        8 * s // element_type_bitwidth
        for s in reversed(mgpu.SwizzlingMode)
        if 8 * s // element_type_bitwidth <= N // n_lane_groups
    )
    if b_is_transposed:
      constraints.append(cs.Divides(b_var, (max_swizzle_elems, 8)))
    else:
      constraints.append(cs.Divides(b_var, (8, max_swizzle_elems)))

  if _is_tmem_ref(op.a):
    a = ValueSite(op, VariableType.OPERAND, 1)
    a_type = ir.ShapedType(op.a.type)
    a_var = ctx.producer_ref(a)
    packing = 32 // utils.bitwidth(a_type.element_type)
    a_layout = tcgen05._infer_tmem_layout(
        tuple(a_type.shape), bool(op.collective), packing
    )
    a_layout = cs.TMEMLayout(a_layout)
    assignments[a_var] = a_layout
    operands_for_variable[a_var] = [a]
    a_is_valid = cs.is_valid_assignment(a_var, a_layout)
    if not a_is_valid:
      raise ValueError(
          f"Cannot assign TMEM layout {a_layout.value} to the 'a' operand of"
          f" a tcgen05 MMA op: the layout is not compatible with the operand"
          f" shape {a.shape}."
      )
  else:
    assert _is_smem_ref(op.a)
    a_is_transposed = utils.is_memref_transposed(ir.MemRefType(op.a.type))
    a = ValueSite(op, VariableType.OPERAND, 1)
    a_var = ctx.producer_ref(a)
    operands_for_variable[a_var] = [a]
    if a_is_transposed:
      constraints.append(cs.IsValidMmaTiling(cs.Transpose(a_var, (1, 0)), element_type_bitwidth))
    else:
      constraints.append(cs.IsValidMmaTiling(a_var, element_type_bitwidth))

  if (sparse_meta_operand := getattr(op, "a_sparse_metadata")) is not None:
    sparse_meta = ValueSite(
        op, VariableType.OPERAND, list(op.operands).index(sparse_meta_operand)
    )
    sparse_meta_var = ctx.producer_ref(sparse_meta)
    sparse_meta_layout = cs.TMEMLayout(tcgen05.sparse_meta_layout())
    assignments[sparse_meta_var] = sparse_meta_layout
    if not cs.is_valid_assignment(sparse_meta_var, sparse_meta_layout):
      raise ValueError(
          f"Cannot assign TMEM layout {sparse_meta_layout.value} to the"
          f" 'a_sparse_metadata' operand of a tcgen05 MMA op: the layout is not"
          f" compatible with the operand shape {sparse_meta.shape}."
      )
    operands_for_variable[sparse_meta_var] = [sparse_meta]

  if (scaled := op.a_scale is not None) != (op.b_scale is not None):
    raise ValueError(
        f"Expecting neither or both scales to be present. Got {op.a_scale=},"
        f" {op.b_scale=}"
    )

  def assign_scaled_layout(scale_operand):
    scale_index = list(op.operands).index(scale_operand)
    scale = ValueSite(op, VariableType.OPERAND, scale_index)
    scale_var = ctx.producer_ref(scale)
    if op.collective and scale_operand == op.b_scale and M == 64:
      layout = tcgen05.b_scales_m64_collective_layout()
    else:
      layout = tcgen05.scales_layout()
    layout = cs.TMEMLayout(layout)
    assignments[scale_var] = layout
    if not cs.is_valid_assignment(scale_var, layout):
      raise ValueError(
          f"Cannot assign {layout} to {scale_operand=} with"
          f" shape {scale.shape}."
      )
    operands_for_variable[scale_var] = [scale]

  if scaled:
    assign_scaled_layout(op.a_scale)
    assign_scaled_layout(op.b_scale)

  return cs.ConstraintSystem(assignments=assignments, constraints=constraints), operands_for_variable

