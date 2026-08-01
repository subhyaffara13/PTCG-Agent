
def vector_concat(
    vectors: Sequence[ir.Value[ir.VectorType]],
) -> ir.Value[ir.VectorType]:
  if not vectors:
    raise ValueError("Cannot concatenate an empty list of vectors")
  vty = vectors[0].type
  if not isinstance(vty, ir.VectorType):
    raise ValueError("Cannot concatenate non-vector values")
  vty = ir.VectorType(vty)
  if vty.rank != 1:
    raise NotImplementedError("Only 1D vectors are supported")
  for v in vectors:
    if v.type.element_type != vty.element_type:
      raise ValueError("Cannot concatenate vectors of different element types")
    if v.type.rank != 1:
      raise ValueError("Can only concatenate 1D vectors")
  return _vector_concat_rec(vectors)

