
def _try_array_cast(arr, dtype):
  if dtype is not None:
    if utils.is_scalar(arr):
      arr = np.asarray(arr).astype(dtype).item()
    else:
      if hasattr(arr, 'astype'):
        arr = arr.astype(dtype)
  return arr

