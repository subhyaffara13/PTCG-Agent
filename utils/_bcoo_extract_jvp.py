
def _bcoo_extract_jvp(arr_dot, indices, arr, *, assume_unique):
  assert arr_dot.shape == arr.shape
  return _bcoo_extract(indices, arr_dot, assume_unique=assume_unique)

