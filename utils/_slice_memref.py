
def _slice_memref(
    ref: ir.Value,
    indexer: NDIndexer,
    ref_aval: state.AbstractRef,
    ref_block_shape: tuple[int | pallas_core.Squeezed, ...],
) -> tuple[ir.Value, tuple[int | pallas_core.Squeezed, ...]]:
  assert ref_block_shape is not None
  starts, sizes, strides, squeeze_dims, ref_block_shape = (
      _indexer_to_start_size_stride(
          indexer,
          ref_block_shape,
          cast_to_index=False,
      )
  )
  if not all((s is None or s == 1) for s in strides):
    raise NotImplementedError("Strided slices of references are unsupported.")

  ir_dynamic_size = ir.ShapedType.get_dynamic_size()
  static_starts: list[int] = []
  for s in starts:
    if not isinstance(s, ir.Value):
      static_starts.append(s)
    elif (v := _fold_and_get_constant_value(s)) is not None:
      static_starts.append(v)
    else:
      static_starts.append(ir_dynamic_size)

  static_sizes: list[int] = []
  dynamic_sizes: list[ir.Value] = []
  for s in sizes:
    if not isinstance(s, ir.Value):
      static_sizes.append(s)
    elif (v := _fold_and_get_constant_value(s)) is not None:
      static_sizes.append(v)
    else:
      static_sizes.append(ir_dynamic_size)
      dynamic_sizes.append(s)

  ref_ty = ir.MemRefType(ref.type)
  out_ty = ir.MemRefType.get(
      static_sizes, ref_ty.element_type, memory_space=ref_ty.memory_space
  )
  out = tpu.memref_slice(out_ty, ref, starts, dynamic_sizes)
  if any(squeeze_dims):
    # We need to squeeze out some dimensions.
    ref_ty = out_ty
    del out_ty
    out_ty = ir.MemRefType.get(
        [dim for i, dim in enumerate(ref_ty.shape) if not squeeze_dims[i]],
        ref_ty.element_type,
        memory_space=ref_ty.memory_space
    )
    out = tpu.memref_squeeze(out_ty, out)
  return out, ref_block_shape

