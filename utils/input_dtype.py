
def input_dtype(x, *_, out_dtype=None, **__):
  if out_dtype is not None:
    return dtypes.canonicalize_dtype(out_dtype)
  return x.dtype

