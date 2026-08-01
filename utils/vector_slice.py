
def vector_slice(v: ir.Value, s: slice):
  v_ty = ir.VectorType(v.type)
  if len(v_ty.shape) != 1:
    raise NotImplementedError(f"Only 1D vectors are supported {v_ty}")
  [v_len] = v_ty.shape
  slice_length = len(range(v_len)[s])
  return vector.extract_strided_slice(
      ir.VectorType.get((slice_length,), v_ty.element_type),
      v,
      [s.start or 0],
      [slice_length],
      [1],
  )

