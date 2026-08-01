
def dtype_np_to_torch(dtype):
  """Returns the torch dtype for the given numpy dtype."""
  return _np_to_torch_dtypes()[np.dtype(dtype)]

