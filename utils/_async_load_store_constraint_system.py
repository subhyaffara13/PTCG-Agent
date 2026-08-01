
def _async_load_store_constraint_system(
    ctx: DerivationContext,
    op: mgpu.AsyncLoadOp | mgpu.AsyncStoreOp,
) -> ConstraintSystemDerivationRuleResult:
  # We only support 2D gathers/scatters along the leading dimension. Tiling
  # either keeps the gather/scatter dimension leading or allows
  # collapsing leading dimensions to maintain contiguity without
  # transforming global memory.
  tiling_multiple = []
  for i, (size, index) in enumerate(zip(op.slice_lengths, op.indices, strict=True)):
    if size == -1:
      # This dimension does not appear in the final smem memref shape.
      continue
    if isinstance(index.type, ir.VectorType):
      if i != 0:
        raise NotImplementedError("Only leading gather dimensions allowed.")
      if isinstance(op, mgpu.AsyncStoreOp):
        gmem_shape = ir.MemRefType(op.destination.type).shape
      else:
        gmem_shape = ir.MemRefType(op.source.type).shape
      if len(gmem_shape) != 2:
        raise NotImplementedError("Only 2D gathers/scatters for async load/store are supported.")
      tiling_multiple.append(size)
      continue
    tiling_multiple.append(dynamic_gcd(size, index))

  operand_index = 1 if isinstance(op, mgpu.AsyncLoadOp) else 0
  operand = ValueSite(op, VariableType.OPERAND, operand_index)
  var = ctx.producer_ref(operand)
  constraints: list[cs.Divides | cs.MinorDimDivisibleBy] = [
      cs.Divides(expr=var, tiling_multiple=tuple(tiling_multiple))
  ]
  if any(isinstance(idx.type, ir.VectorType) for idx in op.indices):
    element_bitwidth = utils.bitwidth(op.source.type.element_type)
    # This constraint enforces sufficient SMEM-alignment.
    # The transfer chunk needs to be 1024 bit-aligned. For each write in the
    # lowering we transfer 4 rows, so each row must be 256 bit-aligned.
    divisor = (1024 // 4) // element_bitwidth
    slice_lengths = [s for s in op.slice_lengths if s != -1]
    if slice_lengths and (slice_lengths[-1] % divisor):
      raise ValueError(
          "Cannot assign layout to async load with gather indices since"
          f" minor dim={slice_lengths[-1]} is not divisible by {divisor=}"
          " bits."
      )
    constraints.append(cs.MinorDimDivisibleBy(expr=var, divisor=divisor))

  value_sites_for_variable = {var: [operand]}
  value_sites, assignments = _vector_value_sites_and_assignments_for_async_ops(op)
  value_sites_for_variable.update(value_sites)
  return cs.ConstraintSystem(assignments, constraints), value_sites_for_variable

