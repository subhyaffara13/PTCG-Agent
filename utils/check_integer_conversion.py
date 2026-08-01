
def check_integer_conversion(arr: Array):
  if not (arr.shape == () and dtypes.issubdtype(arr.dtype, np.integer)):
    raise TypeError("Only integer scalar arrays can be converted to a scalar index.")

