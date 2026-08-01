
def async_copy_sparse_metadata_smem_to_tmem(
    smem_ref: ir.Value, tmem_ref: TMEMRef, collective: bool = False
) -> None:
  i8 = ir.IntegerType.get_signless(8)
  i32 = ir.IntegerType.get_signless(32)
  smem_ty = ir.MemRefType(smem_ref.type)
  if (dtype := smem_ty.element_type) != tmem_ref.dtype:
    raise ValueError(f"Incompatible dtypes: SMEM has {dtype}, TMEM has {tmem_ref.dtype}")
  if dtype != ir.IntegerType.get_signless(2):
    raise NotImplementedError(f"Unsupported dtype: {dtype}, only i2 supported")
  if tmem_ref.shape[0] % 128:
    raise ValueError(f"TMEM reference must have a multiple of 128 rows, but got {tmem_ref.shape[0]}")
  if tmem_ref.shape[1] % 64:
    raise ValueError(f"TMEM reference must have a multiple of 64 colums, but got {tmem_ref.shape[1]}")
  if tmem_ref.layout != sparse_meta_layout():
    raise ValueError(f"TMEM layout {tmem_ref.layout} is not supported")
  smem_shape = tuple(smem_ty.shape)
  expected_smem_shape = (tmem_ref.shape[0] // 128, tmem_ref.shape[1] // 64, 128, 64)
  if smem_shape != expected_smem_shape:
    raise NotImplementedError(
        f"SMEM has {smem_shape}, but expected {expected_smem_shape} for TMEM"
        f" ref shape {tmem_ref.shape}"
    )
  strides, _ = smem_ty.get_strides_and_offset()
  if strides != utils.get_contiguous_strides(smem_shape):
    raise ValueError("Only copies from contiguous SMEM references are supported")
  if expected_smem_shape[0] != 1:
    raise NotImplementedError("Only M=128 supported")
  k_tile_stride = strides[1]
  if k_tile_stride % 16:
    raise ValueError("K tile stride must be a multiple of 16")
  k_tile_byte_stride = k_tile_stride // 4
  for k_tile in range(expected_smem_shape[1]):
    load_ptr = utils.getelementptr(
        utils.memref_ptr(smem_ref), [k_tile * k_tile_byte_stride], i8
    )
    store_ptr = arith.addi(tmem_ref.address, arith.constant(i32, 4 * k_tile))
    # The "core matrix" here is the same as in MMA: 8x(16 bytes).
    desc = mma_utils.encode_descriptor(load_ptr, 0, 8 * 16, swizzle=None)
    ptr = _tmem_addr_to_ptr(store_ptr)
    nvvm.tcgen05_cp(
        nvvm.Tcgen05CpShape.SHAPE_128x128b, ptr, desc,
        group=nvvm.CTAGroupKind.CTA_2 if collective else nvvm.CTAGroupKind.CTA_1
    )

