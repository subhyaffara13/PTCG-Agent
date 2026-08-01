
def _memref_collapse_shape_op_lowering_rule(
    ctx: LoweringContext, op: memref.CollapseShapeOp
) -> Sequence[ir.Value]:
  del ctx

  [in_transforms_attr] = inference_utils.in_transforms(op)
  [out_transforms_attr] = inference_utils.out_transforms(op)

  in_swizzle = swizzle_from_transforms_attr(in_transforms_attr)
  in_transforms = memref_transforms_from_transforms_attr(in_transforms_attr)
  out_swizzle = swizzle_from_transforms_attr(out_transforms_attr)
  out_transforms = memref_transforms_from_transforms_attr(out_transforms_attr)

  if in_swizzle != out_swizzle:
    raise ValueError(
        f"Swizzle mismatch. In transforms swizzle: {in_swizzle}, out transforms"
        f" swizzle {out_swizzle}."
    )
  _check_collapse_shape(op, in_transforms, out_transforms)
  reassociation = [
      [ir.IntegerAttr(i).value for i in ir.ArrayAttr(dims)]
      for dims in op.reassociation
  ]
  new_reassociation = reassociation.copy()
  if in_transforms:
    [t_in] = in_transforms
    assert isinstance(t_in, lc.TileTransform)
    tiling_rank = to_process =  len(t_in.tiling)
    for index_from_end, dims in enumerate(reassociation[::-1]):
      to_process -= len(dims)
      if to_process < 0:
        # This should be caught by `_check_collapse_shape` today, but we check
        # it here as well in case `cs.CollapseShape` ever changes to allow this.
        raise ValueError(
            f"Reassociation {reassociation} is not compatible with tiling "
            f"{t_in.tiling}, as it causes tiled and untiled dimensions to "
            "be collapsed together"
        )
      if to_process == 0:
        for t_dims in reassociation[-index_from_end - 1:]:
          new_reassociation.append([dim + tiling_rank for dim in t_dims])
        break
    assert to_process == 0

  result = memref.collapse_shape(
      transform_type(op.result.type, out_transforms),
      unwrap_transformed_memref(op.src, in_transforms_attr),
      new_reassociation,
  )
  return [wrap_transformed_memref(result, op.result.type, out_transforms_attr)]

