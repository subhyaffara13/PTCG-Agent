
def async_copy_smem_to_tmem(
    smem_ref: _Ref,
    tmem_ref: _Ref,
    collective_axis: AxisName | None = None,
):
  """Copies data from SMEM to TMEM using the tcgen05.cp instruction.

  The source SMEM ref must have tiling and swizzle transforms applied. The
  destination TMEM ref must use packed layout (i.e. ``packed=True`` for sub-32b
  types).

  The copy is performed asynchronously. It can be awaited by calling
  ``tcgen05_commit_arrive`` and waiting on the specified barrier. No
  synchronization is necessary if the target of the copy is used by a
  tcgen05_mma operation.

  Args:
    smem_ref: The SMEM reference to copy from.
    tmem_ref: The TMEM reference to copy into.
    collective_axis: The name of the cluster axis along which the
      copy should be performed collectively. The cluster axis should have a
      size of exactly 2, and must be on the minormost cluster axis.
  """
  smem_ref, smem_transforms = state_primitives.get_ref_and_transforms(
      smem_ref, None, "async_copy_smem_to_tmem"
  )
  flat_smem_transforms, smem_transforms_treedef = tree_util.tree_flatten(
      smem_transforms
  )
  tmem_ref, tmem_transforms = state_primitives.get_ref_and_transforms(
      tmem_ref, None, "async_copy_smem_to_tmem"
  )
  flat_tmem_transforms, tmem_transforms_treedef = tree_util.tree_flatten(
      tmem_transforms
  )
  async_copy_smem_to_tmem_p.bind(
      smem_ref, tmem_ref, *flat_smem_transforms, *flat_tmem_transforms,
      smem_tree=smem_transforms_treedef, tmem_tree=tmem_transforms_treedef,
      collective_axis=collective_axis,
  )


def async_copy_smem_to_tmem(
    smem_ref: ir.Value,
    tmem_ref: TMEMRef,
    swizzle: int,
    collective: bool = False,
) -> None:
  i8 = ir.IntegerType.get_signless(8)
  i32 = ir.IntegerType.get_signless(32)
  smem_ty = ir.MemRefType(smem_ref.type)
  if (dtype := smem_ty.element_type) != tmem_ref.dtype:
    raise ValueError(f"Incompatible dtypes: SMEM has {dtype}, TMEM has {tmem_ref.dtype}")
  if swizzle not in {16, 32, 64, 128}:
    raise ValueError(f"Unsupported swizzle, expected 16, 32, 64 or 128, but got: {swizzle}")
  bitwidth = utils.bitwidth(dtype)
  if tmem_ref.packing != 32 // bitwidth:
    raise ValueError(
        "tcgen05.cp only supports fully packed TMEM references"
        f" (packing={32 // bitwidth}), but got packing={tmem_ref.packing}"
    )
  if tmem_ref.shape[0] != TMEM_ROWS:
    raise ValueError(
        f"TMEM reference must have {TMEM_ROWS} rows, but got {tmem_ref.shape[0]}"
    )
  if tmem_ref.layout != tmem_default_layout(packing=tmem_ref.packing):
    raise ValueError(
        f"Only standard TMEM layout is supported, got: {tmem_ref.layout}"
    )
  swizzle_elems = 8 * swizzle // bitwidth
  expected_smem_shape = utils.tile_shape(tmem_ref.shape, (8, swizzle_elems))
  smem_shape = tuple(smem_ty.shape)
  if smem_shape != expected_smem_shape:
    raise ValueError(
        f"SMEM has shape {smem_shape}, but expected {expected_smem_shape} for"
        f" TMEM shape {tmem_ref.shape} with swizzle={swizzle}"
    )
  strides, _ = smem_ty.get_strides_and_offset()
  row_tile_stride, col_tile_stride, inner_row_stride, inner_col_stride = strides
  if inner_col_stride != 1 or inner_row_stride != swizzle_elems:
    raise ValueError("The SMEM tiles must be contiguous")
  # Make sure strides are a multiple of the byte packing for narrow types.
  byte_packing = max(8 // bitwidth, 1)
  assert row_tile_stride % byte_packing == 0
  assert col_tile_stride % byte_packing == 0

  # Figure out the matrix descriptor parameters (LBO/SBO)
  # The copy happens using the usual "core matrix" structure: a memory region
  # describing a 8x128bit matrix. LBO describes how far apart from each other
  # are consecutive matrices along the minor dimension (in our case the minor
  # dim is contiguous, so exactly 128 bit = 16 bytes apart). SBO describes how
  # far apart is the beginning of the next matrix along the major dimension.
  # We use a tiling of 8, so it is simply the tile stride.
  leading_byte_offset = 16
  stride_byte_offset = row_tile_stride * bitwidth // 8
  assert tmem_ref.shape[1] * bitwidth // 8 >= 16
  if swizzle == 16:
    cp_shape = nvvm.Tcgen05CpShape.SHAPE_128x128b
    cp_cols_bytes = 16  # 128 bit = 16 bytes
  else:
    cp_shape = nvvm.Tcgen05CpShape.SHAPE_128x256b
    cp_cols_bytes = 32  # 256 bit = 32 bytes

  minor_elems_per_cp = cp_cols_bytes * 8 // bitwidth
  num_smem_minor_tiles = smem_shape[1]
  cps_per_smem_minor_tile = swizzle_elems // minor_elems_per_cp
  col_tile_byte_stride = col_tile_stride * bitwidth // 8
  smem_base_ptr = utils.memref_ptr(smem_ref)
  group = (
      nvvm.CTAGroupKind.CTA_2 if collective else nvvm.CTAGroupKind.CTA_1
  )
  for smem_minor_tile in range(num_smem_minor_tiles):
    for cp_idx in range(cps_per_smem_minor_tile):
      smem_byte_offset = (
          smem_minor_tile * col_tile_byte_stride + cp_idx * cp_cols_bytes
      )
      load_ptr = utils.getelementptr(smem_base_ptr, [smem_byte_offset], i8)
      tmem_cols_per_cp = cp_cols_bytes // 4
      tmem_col = (
          smem_minor_tile * cps_per_smem_minor_tile + cp_idx
      ) * tmem_cols_per_cp
      store_addr = arith.addi(tmem_ref.address, arith.constant(i32, tmem_col))
      desc = mma_utils.encode_descriptor(
          load_ptr, leading_byte_offset, stride_byte_offset, swizzle
      )
      nvvm.tcgen05_cp(
          cp_shape, _tmem_addr_to_ptr(store_addr), desc, group=group
      )

