
def _make_shaped_array_for_numpy_scalar(x: np.generic) -> ShapedArray:
  dtype = np.dtype(x)
  dtypes.check_valid_dtype(dtype)
  shape = np.shape(x)
  return ShapedArray(shape, dtypes.canonicalize_dtype(dtype), sharding=None)

