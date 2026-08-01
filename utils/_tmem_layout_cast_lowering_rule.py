
def _tmem_layout_cast_lowering_rule(
    ctx: LoweringContext,
    op: mgpu.TmemLayoutCastOp,
) -> Sequence[ir.Value]:
  del ctx
  in_layout = inference_utils.in_tmem_layouts(op)[0]
  tmem_ref = _tmem_ref_from_ir(op.ref, in_layout)
  # We can't relayout TMEM.
  assert layouts_lib.to_layout_attr(tmem_ref.layout) == op.new_layout
  return [op.ref]

