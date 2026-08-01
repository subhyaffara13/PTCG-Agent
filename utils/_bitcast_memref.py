
def _bitcast_memref(
    ref: ir.Value,
    bitcaster: state_types.BitcastTransform,
    ref_aval: state.AbstractRef,
    ref_block_shape: tuple[int | pallas_core.Squeezed, ...],
) -> tuple[ir.Value, tuple[int | pallas_core.Squeezed, ...]]:
  src_bitwidth = dtypes.itemsize_bits(ref_aval.dtype)
  dst_bitwidth = dtypes.itemsize_bits(bitcaster.dtype)
  if src_bitwidth != dst_bitwidth:
    if len(ref_block_shape) < 2:
      raise NotImplementedError(
          "Bitcast 1D ref with bitwidth change is not supported."
      )
    if ref_block_shape[-2] is pallas_core.squeezed:
      raise NotImplementedError(
          "Bitcast a ref whose 2nd minormost dimension is squeezed when"
          " bitwidth changes."
      )
  out_aval = bitcaster.transform_type(ref_aval)
  ref_ty = ir.MemRefType(ref.type)
  target_ref_ty = ir.MemRefType.get(
      out_aval.shape,
      _dtype_to_ir_type(out_aval.dtype),
      memory_space=ref_ty.memory_space,
  )
  new_ref_block_shape = list(ref_block_shape)
  if (
      len(new_ref_block_shape) >= 2
      and new_ref_block_shape[-2] is not pallas_core.squeezed
  ):
    new_ref_block_shape[-2] = (
        # pyrefly: ignore[unsupported-operation]  # pyrefly#1094
        new_ref_block_shape[-2] * src_bitwidth // dst_bitwidth
    )
  return (
      tpu.memref_bitcast(target_ref_ty, ref),
      tuple(new_ref_block_shape),
  )

