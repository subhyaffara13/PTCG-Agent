
def _compute_swizzle(
    ty: ir.Type, tile_transform: lc.TileTransform | None
) -> mgpu.SwizzlingMode:
  """Computes the swizzle mode given a tiling transform and a data type."""
  if tile_transform is None:
    # TODO(b/447079781): Revisit if this is the behavior we want.
    return mgpu.SwizzlingMode.kNoSwizzle

  if not isinstance(ty, ir.MemRefType):
    raise ValueError(f"Expected a MemRefType, got {ty}.")
  ref_ty = ir.MemRefType(ty)
  strides, _ = ref_ty.get_strides_and_offset()
  tiling = tile_transform.tiling

  if len(tiling) > len(strides):
    raise ValueError(
        f"The tile rank ({len(tiling)}) cannot be greater than the ref's rank"
        f" ({len(strides)})."
    )

  minor_tiling = tiling[np.argmin(strides[-len(tiling):])]
  elem_bitwidth = utils.bitwidth(ref_ty.element_type)
  tiling_bitwidth = minor_tiling * elem_bitwidth
  if tiling_bitwidth % 8:
    raise ValueError("Minor tiling dimension is not byte aligned. "
                     f"Got {minor_tiling} elements of {elem_bitwidth} bits.")
  tiling_bytewidth = tiling_bitwidth // 8
  # Do not swizzle if the bytewidth of the minor tiling dimension does not
  # exactly match a swizzle width.
  if tiling_bytewidth in [128, 64, 32]:
    return mgpu.SwizzlingMode(tiling_bytewidth)
  return mgpu.SwizzlingMode.kNoSwizzle

