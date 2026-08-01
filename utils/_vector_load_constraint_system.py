
def _vector_load_constraint_system(
    ctx: DerivationContext,
    op: mgpu.VectorLoadOp,
) -> ConstraintSystemDerivationRuleResult:
  # Registers
  dest = ValueSite(op, VariableType.RESULT, 0)
  dest_var = cs.Variable(dest)
  value_sites_for_variable = {dest_var: [dest]}
  constraints: list[cs.Constraint]
  constraints = [cs.NotOfType(dest_var, fa.WGSplatFragLayout)]

  if op.optimized is None or op.optimized:
    optimized = cs.OptimizedTransferKind.OPTIMIZED
  else:
    optimized = cs.OptimizedTransferKind.UNOPTIMIZED

  # SMEM
  if _is_smem_ref(op.source):
    source = ValueSite(op, VariableType.OPERAND, 0)
    source_var = ctx.producer_ref(source)
    value_sites_for_variable[source_var] = [source]
    ref_ty = ir.MemRefType(op.source.type)
    shape = tuple(ref_ty.shape)
    strides, _ = ref_ty.get_strides_and_offset()
    constraints.append(
        cs.IsTransferableSmemRegisters(
            source_var, dest_var, shape, tuple(strides),
            bitwidth=utils.bitwidth(ref_ty.element_type),
            optimized=optimized
        )
    )

  system = cs.ConstraintSystem(constraints=constraints)
  return system, value_sites_for_variable

