
def dtype_torch_to_np(dtype) -> np.dtype:
  """Returns the numpy dtype for the given torch dtype."""
  return _torch_to_np_dtypes()[dtype]

