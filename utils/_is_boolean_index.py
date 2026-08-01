
def _is_boolean_index(i):
  try:
    abstract_i = core.typeof(i)
  except TypeError:
    abstract_i = None
  return (isinstance(abstract_i, core.ShapedArray) and dtypes.issubdtype(abstract_i.dtype, np.bool_)
          or isinstance(i, list) and i and all(_is_scalar(e)
          and dtypes.issubdtype(dtypes.dtype(e), np.bool_) for e in i))

