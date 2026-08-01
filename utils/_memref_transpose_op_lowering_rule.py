
def _memref_transpose_op_lowering_rule(
    ctx: LoweringContext, op: memref.TransposeOp
) -> Sequence[ir.Value]:
  del ctx

  in_transforms_attr = inference_utils.in_transforms(op)[0]
  unwrapped_in_ref = unwrap_transformed_memref(op.in_, in_transforms_attr)
  in_swizzle = swizzle_from_transforms_attr(in_transforms_attr)
  in_transforms = memref_transforms_from_transforms_attr(in_transforms_attr)
  out_transforms_attr = inference_utils.out_transforms(op)[0]
  out_swizzle = swizzle_from_transforms_attr(out_transforms_attr)
  out_transforms = memref_transforms_from_transforms_attr(out_transforms_attr)

  if in_swizzle != out_swizzle:
    raise ValueError(
        f"Swizzle mismatch. In transforms swizzle: {in_swizzle}, out transforms"
        f" swizzle {out_swizzle}."
    )
  if len(out_transforms) != len(in_transforms):
    raise ValueError(
        f"Size mismatch for in/out transforms. In transforms: {in_transforms},"
        f" out transforms: {out_transforms}."
    )
  if not out_transforms:
    new_permutation = op.permutation
  else:
    permutation = [
        ir.AffineDimExpr(e).position
        for e in op.permutation.value.results
    ]
    # We expect to have the same transforms on in/out, up to permutation of the
    # out transforms.
    # For example, for 3D input:
    #   permutation: (0, 2, 1)
    #   in_transforms: TilingTransform((32, 8))
    # We expect:
    #   out_transforms: TilingTransform((8, 32))
    # TODO(olechwierowicz): Support multiple transforms.
    [transform] = out_transforms
    [in_transform] = in_transforms
    if not isinstance(transform, lc.TileTransform) or not isinstance(
        in_transform, lc.TileTransform
    ):
      raise NotImplementedError(
          f"Unsupported in/out transforms. In transform: {in_transform}, out"
          f" transform: {transform}"
      )
    tiling_len = len(in_transform.tiling)
    tiling_offset = len(permutation) - tiling_len
    if any(dim < tiling_offset for dim in permutation[-tiling_len :]):
      raise ValueError(
          f"Cannot tile a transpose ({permutation}). Tiling dims"
          f" ({permutation[-tiling_len:]}) cannot contain non-tiled dims."
          f" All of them must be >= {tiling_offset}."
      )
    dims = [-1] * len(permutation)
    dims = dims[:-tiling_len] + list(in_transform.tiling)
    permuted_dims = tuple(dims[permutation[i]] for i in range(len(dims)))
    if permuted_dims[-tiling_len:] != transform.tiling:
      raise ValueError(
          f"Invalid in/out transforms. In transform: {in_transform}, out"
          f" transform: {transform}"
      )
    new_permutation = permutation + [
        x + tiling_len for x in permutation[-tiling_len:]
    ]
    new_permutation = _permutation_to_affine_map_attr(new_permutation)

  new_transpose_op = memref.TransposeOp(
      transform_type(ir.MemRefType(op.result.type), out_transforms),
      unwrapped_in_ref,
      new_permutation,
  )

  out_transforms = inference_utils.out_transforms(op)[0]
  wrapped_ref = wrap_transformed_memref(
      new_transpose_op.result, op.result.type, out_transforms
  )
  return [wrapped_ref]

