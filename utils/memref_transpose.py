
def memref_transpose(ref: ir.Value, permutation: Sequence[int]) -> ir.Value:
  ref_ty = ir.MemRefType(ref.type)
  strides, offset = ref_ty.get_strides_and_offset()
  new_strides = [strides[p] for p in permutation]
  new_shape = [ref_ty.shape[p] for p in permutation]
  new_layout = ir.StridedLayoutAttr.get(offset, new_strides)
  new_ty = ir.MemRefType.get(
      new_shape, ref_ty.element_type, new_layout, ref_ty.memory_space
  )
  return memref.transpose(
      new_ty, ref, ir.AffineMap.get_permutation(permutation)
  )

