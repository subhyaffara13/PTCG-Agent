
def _mgpu_with_transforms_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.WithTransformsOp
) -> Sequence[ir.Value]:
  """Lowering rule for mgpu.WithTransformsOp.
  This is a noop that simply returns its input.
  """
  del ctx

  [in_transforms] = inference_utils.in_transforms(op)
  unwrapped_source_ref = unwrap_transformed_memref(op.ref, in_transforms)
  out_transforms = inference_utils.out_transforms(op)[0]
  wrapped_ref = wrap_transformed_memref(
      unwrapped_source_ref, op.result.type, out_transforms
  )
  return [wrapped_ref]

