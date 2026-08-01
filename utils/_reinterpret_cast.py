
def _reinterpret_cast(ref: ir.Value, new_ref_aval: state_types.AbstractRef) -> ir.Value:
  ref_ty = ir.MemRefType(ref.type)
  strides, offset = ref_ty.get_strides_and_offset()
  # A sanity check. It doesn't do much to check that an offset is dynamic, but
  # if we ever get here through an unexpected path that slices with a non-zero
  # static offset, we'll at least catch it.
  assert offset == 0  or offset == ir.ShapedType.get_dynamic_stride_or_offset()
  expected_strides = mgpu_utils.get_contiguous_strides(ref_ty.shape)
  if expected_strides != strides:
    raise NotImplementedError(
        f"Expected contiguous strides {expected_strides} when applying "
        f"reinterpret_cast to {ref_ty} but got {strides}"
    )
  if offset == 0:
    layout = None
  else:
    layout = ir.StridedLayoutAttr.get(
        offset, mgpu_utils.get_contiguous_strides(new_ref_aval.shape)
    )
  new_ty = ir.MemRefType.get(
      new_ref_aval.shape, mgpu_utils.dtype_to_ir_type(new_ref_aval.dtype),
      memory_space=ref_ty.memory_space,
      layout=layout
  )
  if new_ty == ref_ty:
    return ref
  return mgpu.dialect.reinterpret_cast(new_ty, ref)

