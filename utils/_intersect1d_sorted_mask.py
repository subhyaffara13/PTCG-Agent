
def _intersect1d_sorted_mask(arr1: Array, arr2: Array,
                             return_indices: bool) -> tuple[Array, Array, Array | None]:
  """JIT-compatible helper function for intersect1d"""
  assert arr1.ndim == arr2.ndim == 1
  arr = concatenate((arr1, arr2))
  if return_indices:
    idx_dtype = lax_utils.int_dtype_for_dim(arr.shape[0], signed=True)
    iota = lax.broadcasted_iota(idx_dtype, np.shape(arr), dimension=0)
    aux, indices = lax.sort_key_val(arr, iota)
  else:
    aux = sort(arr)
    indices = None
  mask = aux[1:] == aux[:-1]
  return aux, mask, indices

