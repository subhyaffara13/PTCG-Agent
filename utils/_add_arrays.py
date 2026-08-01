
def _add_arrays(x, y):
  if (isinstance(a := core.typeof(x), ShapedArray) and
      dtypes.issubdtype(a.dtype, dtypes.extended)):
    return a.dtype._rules.add(dtype, x, y)
  return add(x, y)

