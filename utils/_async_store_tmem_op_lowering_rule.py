
def _async_store_tmem_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.AsyncStoreTmemOp
) -> Sequence[ir.Value]:
  """Lowering rule for mgpu.AsyncStoreTmemOp."""
  del ctx
  in_layout_attr = inference_utils.in_tmem_layouts(op)[0]
  tmem_ref = _tmem_ref_from_ir(op.destination, in_layout_attr)
  in_layout_attr = inference_utils.in_layouts(op)[0]
  arr = _fragmented_array_from_ir(op.source, in_layout_attr)
  tmem_ref.store(arr)

  return []

