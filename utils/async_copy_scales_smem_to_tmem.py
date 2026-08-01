
def async_copy_scales_smem_to_tmem(
    smem_ref: ir.Value, tmem_ref: TMEMRef, collective: bool = False
) -> None:
  """Asynchronously copies the scale data from SMEM to TMEM.

  The result of the copy can be awaited by calling ``commit_arrive`` and waiting
  on the chosen ``Barrier``. However, if TMEM reference is to be consumed by a
  MMA issued in the same thread, no additional synchronization is needed.

  Two TMEM layouts are supported:

  **scales_layout()**: The standard layout for A and B scales. The ``smem_ref``
  must be contiguous with shape ``(MN // 128, K // 4, 32, 16)`` for 8-bit
  scales (here MN is the non-contracting dimension, padded to a multiple of
  128), matching the scale layout for .scale_vec::1X. See
  https://docs.nvidia.com/cuda/parallel-thread-execution/#tcgen05-mma-scale-factor-a-layout-1x
  for more details. If you have a (MN, K // 32) array of scales in JAX (where
  MN is divisible by 32 and K is divisible by 128), you can prepare it this
  way (pad_mn = (MN + 127) // 128 * 128)::

      jnp.pad(scales, ((0, pad_mn - mn), (0, 0)))
        .reshape(pad_mn // 128, 4, 32, k // 4, 4)
        .transpose(0, 3, 2, 1, 4)
        .reshape(pad_mn // 128, k // 4, 32, 16)

  The TMEM ref is expected to have shape ``(pad_mn, K // 32)`` and the layout
  created by ``scales_layout()``.

  **b_scales_m64_collective_layout()**: Used for B scales in 2CTA block-scaled
  MMA with M=128 (64 per CTA). Note that both the SMEM and TMEM layout need N to
  be treated as padded to 256. The ``smem_ref`` must be contiguous with shape
  ``(1, K // 4, 64, 16)``. The TMEM ref is expected to have shape
  ``(256, K // 32)``, no matter how long N is. If you have a (N, K // 32)
  array of B scales in JAX (where N is a multiple of 64), you can prepare them
  this way (columns_per_cta = N // 64)::

      jnp.pad(
          scales.reshape(2, columns_per_cta, 32, k // 4, 4)
          .transpose(3, 0, 2, 1, 4)
          .reshape(1, k // 4, 64, columns_per_cta * 4),
          ((0, 0), (0, 0), (0, 0), (0, 16 - columns_per_cta * 4)),
      )
  """
  i32 = ir.IntegerType.get_signless(32)
  smem_ty = ir.MemRefType(smem_ref.type)
  if (dtype := smem_ty.element_type) != tmem_ref.dtype:
    raise ValueError(f"Incompatible dtypes: SMEM has {dtype}, TMEM has {tmem_ref.dtype}")
  if dtype not in {ir.Float8E8M0FNUType.get(), ir.Float8E4M3FNType.get()}:
    raise ValueError(f"Unsupported dtype: {dtype}, only f8e8m0fnu and f8e4m3fn are supported")
  if tmem_ref.shape[0] % TMEM_ROWS:
    raise ValueError(f"TMEM reference must have a multiple of {TMEM_ROWS} rows, but got {tmem_ref.shape[0]}")
  if tmem_ref.shape[1] % 4:
    raise ValueError(f"TMEM reference must have a multiple of 4 columns, but got {tmem_ref.shape[1]}")

  smem_shape = tuple(smem_ty.shape)
  strides, _ = smem_ty.get_strides_and_offset()
  # TODO(apaszke): This should only matter for the two minor dims.
  if strides != utils.get_contiguous_strides(smem_shape):
    raise ValueError("Only copies from contiguous SMEM references are supported")

  if tmem_ref.layout == b_scales_m64_collective_layout():
    k_tiles = tmem_ref.shape[1] // 4
    expected_smem_shape = (1, k_tiles, 64, 16)
    if smem_shape != expected_smem_shape:
      raise NotImplementedError(
          f"SMEM has shape {smem_shape}, but expected {expected_smem_shape} for"
          f" TMEM ref shape {tmem_ref.shape}"
      )
    k_tile_stride_i32 = strides[1] // 4
    for k_tile in range(k_tiles):
      load_ptr = utils.getelementptr(
          utils.memref_ptr(smem_ref), [k_tile * k_tile_stride_i32], i32
      )
      store_addr = arith.addi(
          tmem_ref.address, arith.constant(i32, 4 * k_tile),
      )
      desc = mma_utils.encode_descriptor(load_ptr, 0, 8 * 16, swizzle=None)
      nvvm.tcgen05_cp(
          nvvm.Tcgen05CpShape.SHAPE_64x128b,
          _tmem_addr_to_ptr(store_addr),
          desc,
          multicast=nvvm.Tcgen05CpMulticast.WARPX2_01_23,
          group=nvvm.CTAGroupKind.CTA_2 if collective else nvvm.CTAGroupKind.CTA_1,
      )
    return

  if tmem_ref.layout != scales_layout():
    raise ValueError(
        f"TMEM layout {tmem_ref.layout} is not supported for scale copies. Only"
        " scales_layout() and b_scales_m64_collective_layout() are supported."
    )

  expected_smem_shape = (tmem_ref.shape[0] // TMEM_ROWS, tmem_ref.shape[1] // 4, 32, 16)
  if smem_shape != expected_smem_shape:
    raise NotImplementedError(
        f"SMEM has {smem_shape}, but expected {expected_smem_shape} for TMEM"
        f" ref shape {tmem_ref.shape}"
    )
  mn_tile_stride, k_tile_stride = strides[:2]
  # One tile of scales has 128 bytes.
  if mn_tile_stride % 128 or k_tile_stride % 128:
    raise ValueError("Scale tile strides must be a multiple of 128")
  mn_tile_stride_i32 = mn_tile_stride // 4
  k_tile_stride_i32 = k_tile_stride // 4
  # TODO(apaszke): Need to figure out the TMEM layout otherwise and MMA doesn't
  # support it anyway.
  if smem_shape[0] > 2:
    raise NotImplementedError("Only M/N up to 256 supported")
  for mn_tile, k_tile in np.ndindex(smem_shape[:2]):
    load_ptr = utils.getelementptr(
        utils.memref_ptr(smem_ref),
        [mn_tile * mn_tile_stride_i32 + k_tile * k_tile_stride_i32],
        i32,
    )
    # NOTE: The tiles are MN-minor in TMEM, but MN-major (logically) in SMEM.
    store_addr = arith.addi(
        tmem_ref.address,
        arith.constant(i32, 4 * smem_shape[0] * k_tile + 4 * mn_tile),
    )
    # The "core matrix" here is the same as in MMA: 8x(16 bytes).
    desc = mma_utils.encode_descriptor(load_ptr, 0, 8 * 16, swizzle=None)
    nvvm.tcgen05_cp(
        nvvm.Tcgen05CpShape.SHAPE_32x128b,
        _tmem_addr_to_ptr(store_addr),
        desc,
        multicast=nvvm.Tcgen05CpMulticast.WARPX4,
        group=nvvm.CTAGroupKind.CTA_2 if collective else nvvm.CTAGroupKind.CTA_1,
    )

