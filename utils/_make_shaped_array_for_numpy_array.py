
def _make_shaped_array_for_numpy_array(x: np.ndarray) -> ShapedArray:
  dtype = x.dtype
  dtypes.check_valid_dtype(dtype)
  return ShapedArray(x.shape, dtypes.canonicalize_dtype(dtype), sharding=None)

