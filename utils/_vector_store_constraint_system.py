
def _vector_store_constraint_system(
    ctx: DerivationContext,
    op: Any,  # This is mgpu.VectorStoreOp | mgpu.AsyncStoreSmemOp
) -> ConstraintSystemDerivationRuleResult:
  # Registers
  value = ValueSite(op, VariableType.OPERAND, 0)
  value_var = cs.Variable(value)
  value_sites_for_variable = {value_var: [value]}

  # Store is a special case in Pallas, where we are willing to downgrade from
  # requiring an optimized transfer in some cases.
  if op.optimized is None:
    optimized = cs.OptimizedTransferKind.DOWNGRADABLE
  elif op.optimized:
    optimized = cs.OptimizedTransferKind.OPTIMIZED
  else:
    optimized = cs.OptimizedTransferKind.UNOPTIMIZED

  # SMEM
  constraints = []
  if _is_smem_ref(op.destination):
    dest = ValueSite(op, VariableType.OPERAND, 1)
    dest_var = ctx.producer_ref(dest)
    value_sites_for_variable[dest_var] = [dest]
    ref_ty = ir.MemRefType(op.destination.type)
    shape = tuple(ref_ty.shape)
    strides, _ = ref_ty.get_strides_and_offset()
    constraints.append(
        cs.IsTransferableSmemRegisters(
            value_var, dest_var, shape, tuple(strides),
            bitwidth=utils.bitwidth(ref_ty.element_type),
            optimized=optimized
        )
    )

  system = cs.ConstraintSystem(constraints=constraints)
  return system, value_sites_for_variable

