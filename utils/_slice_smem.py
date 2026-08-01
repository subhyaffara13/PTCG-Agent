
def _slice_smem(
    result: ir.Type,
    smem_base: ir.Value,
    offset: int,
    lowering_semantics: LoweringSemantics,
) -> ir.Value:
  if lowering_semantics == LoweringSemantics.Warpgroup:
    return dialect.slice_smem(result, offset)
  else:
    ir_offset = arith.constant(ir.IndexType.get(), offset)
    return memref.view(result, smem_base, ir_offset, [])


def _slice_smem(result: ir.MemRefType, offset: int, smem_size: int):
  size = math.prod(result.shape) * utils.bitwidth(result.element_type) // 8
  if offset + size > smem_size:
    raise ValueError("Ran out of shared memory.")

  i8 = ir.IntegerType.get_signless(8)
  smem_base = gpu.dynamic_shared_memory(
      ir.MemRefType.get((utils.DYNAMIC,), i8, memory_space=utils.smem())
  )
  ir_offset = arith.constant(ir.IndexType.get(), offset)
  lowered_result_type = result
  if isinstance(result.element_type, mgpu.BarrierType):
    lowered_result_type = ir.MemRefType.get(
        result.shape, _lowered_barrier_type(), memory_space=utils.smem()
    )
  view = memref.view(lowered_result_type, smem_base, ir_offset, [])
  if result == lowered_result_type:
    return view
  return builtin.unrealized_conversion_cast([result], [view])

