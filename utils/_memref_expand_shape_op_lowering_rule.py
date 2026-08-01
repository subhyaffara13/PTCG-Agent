
def _memref_expand_shape_op_lowering_rule(
    ctx: LoweringContext, op: memref.ExpandShapeOp
) -> Sequence[ir.Value]:
  del ctx

  in_transforms = inference_utils.in_transforms(op)[0]
  unwrapped_in_ref = unwrap_transformed_memref(op.src, in_transforms)
  in_transformed_ty = ir.MemRefType(unwrapped_in_ref.type)

  out_transforms = inference_utils.out_transforms(op)[0]
  out_transformed_ty = transform_type(op.result.type, out_transforms)

  reassociation = cast(list[ir.ArrayAttr], list(op.reassociation))
  num_tiling_dims = len(in_transformed_ty.shape) - len(op.src.type.shape)

  # We don't currently allow expanding tiled dimensions. So to compute the
  # reassociation on the lowered types, we just need to backfill the original
  # one with the number of missing dimensions.
  if num_tiling_dims > 0 and any(
      len(x) > 1 for x in reassociation[-num_tiling_dims:]
  ):
    # If we ever remove this restriction, we will need to ensure this is
    # compatible with `transform_type`.
    raise NotImplementedError("Expanding tiled dimensions is not supported.")

  start_index = len(op.static_output_shape)
  for i in range(start_index, start_index + num_tiling_dims):
    reassociation.append([i])  # pyrefly: ignore[bad-argument-type]

  new_expand_shape_op = memref.ExpandShapeOp(
      out_transformed_ty,
      unwrapped_in_ref,
      reassociation,
      output_shape=op.output_shape,
      static_output_shape=out_transformed_ty.shape,
  )

  wrapped_ref = wrap_transformed_memref(
      new_expand_shape_op.result, op.result.type, out_transforms
  )
  return [wrapped_ref]

