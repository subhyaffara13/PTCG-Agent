
def _async_store_smem_to_tmem_lowering_rule(
    ctx: LoweringContext, op: mgpu.AsyncStoreSmemToTmemOp
) -> Sequence[ir.Value]:
  ctx.check_collective(op)
  [transforms_attr] = inference_utils.in_transforms(op)
  swizzle = swizzle_from_transforms_attr(transforms_attr)
  smem_ref = unwrap_transformed_memref(op.source, transforms_attr)
  smem_ref_ty = op.source.type
  assert isinstance(smem_ref_ty, ir.MemRefType)

  [in_layout_attr] = inference_utils.in_tmem_layouts(op)
  tmem_ref = _tmem_ref_from_ir(op.destination, in_layout_attr)
  with utils.when(ctx.single_lane_predicate):
    tcgen05.async_copy_smem_to_tmem(
        smem_ref, tmem_ref, swizzle, collective=bool(op.collective)
    )
  return []

