
def _split_gmem_slice(gmem_slice):
  i32 = ir.IntegerType.get_signless(32)
  indices = []
  slice_lengths = []
  for idx in gmem_slice:
    match idx:
      case slice():
        indices.append(mgpu.utils.c(idx.start, i32))
        slice_lengths.append(idx.stop - idx.start)
      case mgpu.DynamicSlice():
        indices.append(arith_dialect.index_cast(i32, idx.base))  # pyrefly: ignore[bad-argument-type]
        slice_lengths.append(idx.length)
      case ir.Value() if isinstance(idx.type, ir.IndexType):
        indices.append(arith_dialect.index_cast(i32, idx))
        slice_lengths.append(-1)
      case ir.Value() if isinstance(idx.type, ir.IntegerType):
        indices.append(idx)
        slice_lengths.append(-1)
      case ir.Value() if isinstance(idx.type, ir.VectorType):
        indices.append(idx)
        [length] = ir.VectorType(idx.type).shape
        slice_lengths.append(length)
      case _:
        raise NotImplementedError(f"Unsupported GMEM slice: {idx}")
  return indices, slice_lengths

