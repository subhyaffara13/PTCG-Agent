
def _check_collapse_shape(
    op: memref.CollapseShapeOp,
    in_transforms: Sequence[lc.MemRefTransform],
    out_transforms: Sequence[lc.MemRefTransform],
):
  if len(in_transforms) != len(out_transforms):
    raise ValueError(
        "Expected the same number of in/out transforms, but got "
        f"{in_transforms=} and {out_transforms=}"
    )
  if not in_transforms:
    return
  t_in, *in_transforms = in_transforms
  t_out, *_ = out_transforms
  if (in_transforms or
      not isinstance(t_in, lc.TileTransform) or
      not isinstance(t_out, lc.TileTransform)):
    raise NotImplementedError(
        "Only a single tiling transform is supported when collapsing a shape, "
        f"but got {in_transforms=} and {out_transforms=}"
    )
  src_ty = ir.MemRefType(op.src.type)
  strides, _ = src_ty.get_strides_and_offset()
  if strides != utils.get_contiguous_strides(src_ty.shape):
    raise NotImplementedError(
        "Collapsing the shape of a memref with non-contiguous strides is not "
        "supported"
    )
  reassociation = tuple(len(ir.ArrayAttr(idx)) for idx in op.reassociation)

  collapsed_tiling = cs.reduce_expression(
      cs.CollapseShape(cs.SMEMTransforms(t_in), tuple(src_ty.shape),
                       reassociation),
      {},
  )

  if isinstance(collapsed_tiling, cs.Unsatisfiable):
    raise ValueError(f"Input tiling {t_in.tiling} is not compatible with {op}")

  assert isinstance(collapsed_tiling, cs.SMEMTransforms)
  expected_t_out = collapsed_tiling.tiling
  assert expected_t_out is not None
  if expected_t_out != t_out:
    raise ValueError(
        "Input/output tiling mismatch when attempting to collapse a shape. "
        f"Expected output tiling to be {expected_t_out.tiling} for input "
        f"tiling {t_in.tiling}, but got {t_out.tiling}"
    )

