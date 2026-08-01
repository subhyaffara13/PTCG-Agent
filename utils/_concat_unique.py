
def _concat_unique(arr1: Array, arr2: Array) -> tuple[Array, Array]:
  """Utility to concatenate the unique values from two arrays."""
  arr1, arr2 = ravel(arr1), ravel(arr2)
  arr1, num_unique1 = _unique(arr1, axis=0, size=arr1.size, return_true_size=True)
  arr2, num_unique2 = _unique(arr2, axis=0, size=arr2.size, return_true_size=True)
  arr = zeros(arr1.size + arr2.size, dtype=dtypes.result_type(arr1, arr2))
  arr = lax_slicing.dynamic_update_slice(arr, arr1, (0,))
  arr = lax_slicing.dynamic_update_slice(arr, arr2, (num_unique1,))
  return arr, num_unique1 + num_unique2

