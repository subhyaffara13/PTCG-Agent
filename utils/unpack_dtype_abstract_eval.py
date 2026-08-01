
def unpack_dtype_abstract_eval(x):
  if dtypes.issubdtype(x.dtype, FusibleElementDType):
    return x.dtype.abstract_unpack(x)
  elif isinstance(x.dtype, state.AbstractRef):
    raise NotImplementedError()
  raise ValueError("Attempted to unpack non-fusion dtype: {dtype}")

