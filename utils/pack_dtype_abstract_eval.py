
def pack_dtype_abstract_eval(*xs, dtype):
  if dtypes.issubdtype(dtype, FusibleElementDType):
    return dtype.abstract_pack(*xs)
  raise ValueError("Attempted to pack non-fusion dtype: {dtype}")

