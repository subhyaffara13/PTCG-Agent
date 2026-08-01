
def num_float_bits(dtype: DTypeLike) -> int:
  return _dtypes.finfo(_dtypes.canonicalize_dtype(dtype)).bits

