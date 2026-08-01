
def _vector_concat_rec(
    vectors: Sequence[ir.Value[ir.VectorType]],
) -> ir.Value[ir.VectorType]:
  match vectors:
    case [v]:
      return v
    case [v, w]:
      [v_len] = ir.VectorType(v.type).shape
      [w_len] = ir.VectorType(w.type).shape
      mask = ir.DenseI64ArrayAttr.get(list(range(v_len + w_len)))
      return vector.shuffle(*vectors, mask=mask)
    case _:
      assert vectors
      l = _vector_concat_rec(vectors[: len(vectors) // 2])
      r = _vector_concat_rec(vectors[len(vectors) // 2 :])
      return _vector_concat_rec([l, r])

