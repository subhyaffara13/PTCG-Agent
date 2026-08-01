
def _tmem_alloc_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.TmemAllocOp
) -> Sequence[ir.Value]:
  """Lowering rule for mgpu.TmemAllocOp."""
  ctx.check_collective(op)

  output_shape = ir.MemRefType(op.result.type).shape
  ncols = output_shape[1] // op.packing.value

  with utils.when(ctx.single_warp_per_block_predicate):
    tcgen05.tmem_alloc(op.smem_ptr, ncols, bool(op.collective), exact=False)
  gpu.barrier()
  tmem_addr = memref.load(op.smem_ptr, [])

  cast_op = builtin.UnrealizedConversionCastOp(
      [op.result.type], [tmem_addr]
  )
  cast_op.attributes["collective"] = op.collective
  cast_op.attributes["packing"] = op.packing
  cast_op.attributes["layout"] = inference_utils.out_tmem_layouts(op)[0]

  return [cast_op.result]

