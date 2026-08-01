
def _tmem_dealloc_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.TmemDeallocOp
) -> Sequence[ir.Value]:
  """Lowering rule for mgpu.TmemDeallocOp."""
  i32 = ir.IntegerType.get_signless(32)
  conversion_cast, [tmem_addr] = _undo_conversion_cast(op.tmem_ref, [i32])
  collective = ir.BoolAttr(conversion_cast.attributes["collective"]).value
  packing: int = ir.IntegerAttr(conversion_cast.attributes["packing"]).value

  output_shape = ir.MemRefType(op.tmem_ref.type).shape
  ncols = output_shape[1] // packing

  with utils.when(ctx.single_warp_per_block_predicate):
    tcgen05.tmem_dealloc(tmem_addr, ncols, collective, exact=False)

  return []

