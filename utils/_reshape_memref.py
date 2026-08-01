
def _reshape_memref(
    ref: ir.Value,
    reshaper: state_types.ReshapeTransform,
    ref_aval: state.AbstractRef,
    ref_block_shape: tuple[int | pallas_core.Squeezed, ...],
) -> tuple[ir.Value, tuple[int, ...]]:
  if len(ref_block_shape) < 2:
    raise NotImplementedError("Reshape 1D ref is not supported.")
  if (
      ref_block_shape[-2] is pallas_core.squeezed
      or ref_block_shape[-1] is pallas_core.squeezed
  ):
    raise NotImplementedError(
        "Reshape a ref with squeezed dimension on last two dimensions."
    )
  num_elements = math.prod(map(pallas_core.get_block_size, ref_block_shape))
  if num_elements != math.prod(reshaper.shape):
    raise ValueError(
        f"Reshape a ref with different number of elements: {ref_block_shape} "
        f"vs {reshaper.shape}"
    )
  ref_ty = ir.MemRefType(ref.type)
  target_ref_ty = ir.MemRefType.get(
      reshaper.shape,
      _dtype_to_ir_type(ref_aval.dtype),
      memory_space=ref_ty.memory_space,
  )
  return (
      tpu.memref_reshape(target_ref_ty, ref),
      reshaper.shape,
  )

