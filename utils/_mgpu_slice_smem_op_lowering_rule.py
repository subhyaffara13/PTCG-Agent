
def _mgpu_slice_smem_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.SliceSMEMOp
) -> Sequence[ir.Value]:
  ref_ty = ir.MemRefType(op.result.type)
  offset = op.offset.value
  if isinstance(ref_ty.element_type, mgpu.BarrierType):
    # Barrier memrefs are not transformed and must not be wrapped.
    assert not inference_utils.has_out_transforms_set(op)
    return [_slice_smem(ref_ty, offset, ctx.smem_requested_bytes)]

  [out_transforms] = inference_utils.out_transforms(op)
  transformed_ref_ty = transform_type(ref_ty, out_transforms)
  transformed_ref = _slice_smem(transformed_ref_ty, offset, ctx.smem_requested_bytes)
  return [wrap_transformed_memref(transformed_ref, op.result.type, out_transforms)]

