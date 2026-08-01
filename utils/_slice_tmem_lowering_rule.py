
def _slice_tmem_lowering_rule(
    ctx: LoweringContext, op: mgpu.SliceTmemOp
) -> Sequence[ir.Value]:
  del ctx
  in_layout_attr = inference_utils.in_tmem_layouts(op)[0]
  out_layout_attr = inference_utils.out_tmem_layouts(op)[0]
  source = _tmem_ref_from_ir(op.source, in_layout_attr)
  i32 = ir.IntegerType.get_signless(32)
  offset = arith.constant(i32, op.offset)
  dest_addr = arith.addi(source.address, offset)
  conversion_cast = builtin.UnrealizedConversionCastOp([op.result.type], [dest_addr])
  conversion_cast.attributes["layout"] = out_layout_attr
  return [conversion_cast.result]

