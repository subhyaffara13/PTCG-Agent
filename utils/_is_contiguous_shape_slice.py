
def _is_contiguous_shape_slice(
    ref_ty: ir.MemRefType, dim_slice: slice = slice(None)
):
  # If it's not a strided layout then we are definitely contiguous.
  if not isinstance(ref_ty.layout, ir.StridedLayoutAttr):
    return True

  strides = ir.StridedLayoutAttr(ref_ty.layout).strides[dim_slice]
  shape = ref_ty.shape[dim_slice]

  # Check that each dimension fits exactly it the immediately larger stride.
  ss = sorted(zip(strides, shape), key=lambda x: x[0], reverse=True)
  for (prev_stride, _), (stride, shape) in zip(ss, ss[1:]):
    if stride * shape != prev_stride:
      return False

  return True

