import math


def copy_tiled(src: ir.Value, dst: ir.Value, swizzle: int = 16):
  """Copy the data from the src reference to the dst reference.

  Exactly one of src/dst should be in SMEM, while the other should be in GMEM.
  The SMEM reference is expected to be tiled into (8, swizzle_elems) (as it
  would for MMA), and so should have a rank larger by 2 than the GMEM ref.
  """
  src_ty = ir.MemRefType(src.type)
  dst_ty = ir.MemRefType(dst.type)
  if math.prod(src_ty.shape) != math.prod(dst_ty.shape):
    raise ValueError(
        "Source and destination must have the same number of elements, but got"
        f" source shape {src_ty.shape} and destination shape {dst_ty.shape}"
    )
  if src_ty.element_type != dst_ty.element_type:
    raise ValueError(
        "Source and destination must have the same element type, but got"
        f" source type {src_ty.element_type} and destination type"
        f" {dst_ty.element_type}"
    )
  bitwidth = utils.bitwidth(src_ty.element_type)
  # Signedness doesn't matter, but we need to specify something for the
  # intermediate arrays.
  is_signed = False if isinstance(src_ty.element_type, ir.IntegerType) else None
  if utils.is_smem_ref(src_ty) != utils.is_smem_ref(dst_ty):
    if utils.is_smem_ref(src_ty):
      smem_ty, gmem_ty = src_ty, dst_ty
    else:
      smem_ty, gmem_ty = dst_ty, src_ty
    if smem_ty.rank != gmem_ty.rank + 2:
      raise ValueError(
          "SMEM reference must have a rank larger by 2 than the destination"
          f" reference (due to 2D tiling), but got SMEM rank {smem_ty.rank} and"
          f" destination rank {gmem_ty.rank}."
      )
    swizzle_elems = 8 * swizzle // bitwidth
    if smem_ty.shape[-2:] != [8, swizzle_elems]:
      raise NotImplementedError(
          f"For {swizzle=}, expected SMEM tiling to be (8, {swizzle_elems})"
      )
    expected_src_shape = utils.tile_shape(gmem_ty.shape, (8, swizzle_elems))
    if tuple(smem_ty.shape) != expected_src_shape:
      raise ValueError(
          f"Expected SMEM reference to have shape {expected_src_shape} (tiling"
          f" {gmem_ty.shape} by (8, {swizzle_elems})), but got {smem_ty.shape}"
      )
    layout = tiled_copy_smem_gmem_layout(
        *smem_ty.shape[-4:-2], swizzle, bitwidth  # pyrefly: ignore[bad-argument-count]
    )
    if utils.is_smem_ref(src_ty):
      regs = FragmentedArray.load_tiled(src, swizzle, is_signed=is_signed, layout=layout)
      regs.store_untiled(dst, optimized=False)
    else:
      regs = FragmentedArray.load_untiled(src, is_signed=is_signed, layout=layout, optimized=False)
      regs.store_tiled(dst, swizzle)
    return
  raise NotImplementedError(f"Unsupported copy: {src.type} -> {dst.type}")

