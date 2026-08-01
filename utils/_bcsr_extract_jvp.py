
def _bcsr_extract_jvp(arr_dot, indices, indptr, arr):
  assert arr_dot.shape == arr.shape
  return bcsr_extract(indices, indptr, arr_dot)

