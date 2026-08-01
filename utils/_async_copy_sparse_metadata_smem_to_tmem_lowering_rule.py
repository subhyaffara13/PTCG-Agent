
def _async_copy_sparse_metadata_smem_to_tmem_lowering_rule(
    ctx: LoweringContext, op: mgpu.AsyncStoreSparseMetadataSmemToTmemOp
) -> Sequence[ir.Value]:
  ctx.check_collective(op)
  [in_layout_attr] = inference_utils.in_tmem_layouts(op)
  tmem_ref = _tmem_ref_from_ir(op.destination, in_layout_attr)
  smem_ref = unwrap_transformed_memref(op.source, ir.ArrayAttr.get([]))
  with utils.when(ctx.single_lane_predicate):
    tcgen05.async_copy_sparse_metadata_smem_to_tmem(
      smem_ref, tmem_ref, collective=bool(op.collective)
    )
  return []

