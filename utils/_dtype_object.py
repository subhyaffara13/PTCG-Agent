
def _dtype_object(dtype):
  return dtype if isinstance(dtype, _dtype_object_types) else np.dtype(dtype)

