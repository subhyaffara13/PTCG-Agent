
def _async_load_tmem_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.AsyncLoadTmemOp
) -> Sequence[ir.Value]:
  """Lowering rule for mgpu.AsyncLoadTmemOp."""
  del ctx
  in_layout_attr = inference_utils.in_tmem_layouts(op)[0]
  tmem_ref = _tmem_ref_from_ir(op.source, in_layout_attr)
  out_layout_attr = inference_utils.out_layouts(op)[0]
  out_layout = layouts_lib.from_layout_attr(out_layout_attr)
  assert isinstance(out_layout, fa.TiledLayout)
  is_signed = _default_is_signed(ir.MemRefType(op.source.type).element_type)
  arr = tmem_ref.load(out_layout, is_signed)
  return [fragmented_array_to_ir(arr, op.result.type)]

