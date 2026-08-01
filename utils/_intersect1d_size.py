
def _intersect1d_size(arr1: Array, arr2: Array, fill_value: ArrayLike | None, assume_unique: bool,
                      size: int, return_indices: bool) -> Array | tuple[Array, Array, Array]:
  """Jit-compatible helper function for intersect1d with size specified."""
  # Ensured by caller
  assert arr1.ndim == arr2.ndim == 1
  assert arr1.dtype == arr2.dtype

  # First step: we concatenate the unique values of arr1 and arr2.
  # The resulting values are:
  #   num_unique1/num_unique2: number of unique values in arr1/arr2
  #   aux[:num_unique1 + num_unique2] contains the sorted concatenated
  #     unique values drawn from arr1 and arr2.
  #   aux_sorted_indices: indices mapping aux to concatenation of arr1 and arr2
  #   ind1[:num_unique1], ind2[:num_unique2]: indices of sorted unique
  #     values in arr1/arr2
  #   mask: boolean mask of relevant values in aux & aux_sorted_indices
  if assume_unique:
    ind1, num_unique1 = arange(arr1.size), full((), arr1.size)
    ind2, num_unique2 = arange(arr2.size), full((), arr2.size)
    arr = concatenate([arr1, arr2])
    aux, aux_sort_indices = lax.sort([arr, arange(arr.size)], is_stable=True, num_keys=1)
    mask = ones(arr.size, dtype=bool)
  else:
    arr1, ind1, num_unique1 = _unique(arr1, 0, size=arr1.size, return_index=True, return_true_size=True, fill_value=0)
    arr2, ind2, num_unique2 = _unique(arr2, 0, size=arr2.size, return_index=True, return_true_size=True, fill_value=0)
    arr = zeros(arr1.size + arr2.size, dtype=dtypes.result_type(arr1, arr2))
    arr = lax_slicing.dynamic_update_slice(arr, arr1, (0,))
    arr = lax_slicing.dynamic_update_slice(arr, arr2, (num_unique1,))
    mask = arange(arr.size) < num_unique1 + num_unique2
    _, aux, aux_sort_indices = lax.sort([~mask, arr, arange(arr.size)], is_stable=True, num_keys=2)

  # Second step: extract the intersection values from aux
  # Since we've sorted the unique entries in arr1 and arr2, any place where
  # adjacent entries are equal is a value of the intersection.
  # relevant results here:
  #   num_results: number of values in the intersection of arr1 and arr2
  #   vals: array where vals[:num_results] contains the intersection of arr1 and arr2,
  #         and vals[num_results:] contains the appropriate fill_value.
  aux_mask = (aux[1:] == aux[:-1]) & mask[1:]
  num_results = aux_mask.sum()
  if aux.size:
    val_indices = nonzero(aux_mask, size=size, fill_value=aux.size)[0]
    vals = aux.at[val_indices].get(mode='fill', fill_value=0)
  else:
    val_indices = arange(0)
    vals = zeros(size, aux.dtype)
  if fill_value is None:
    vals = where(arange(len(vals)) < num_results, vals, vals.max())
    vals = where(arange(len(vals)) < num_results, vals, vals.min())
  else:
    vals = where(arange(len(vals)) < num_results, vals, fill_value)

  # Third step: extract the indices of the intersection values.
  # This requires essentially unwinding aux_sort_indices and ind1/ind2 to find
  # the appropriate list of indices from the original arrays.
  if return_indices:
    arr1_indices = aux_sort_indices.at[val_indices].get(mode='fill', fill_value=arr1.size)
    arr1_indices = where(arange(len(arr1_indices)) < num_results, arr1_indices, arr1.size)
    arr2_indices = aux_sort_indices.at[val_indices + 1].get(mode='fill', fill_value=arr2.size) - num_unique1
    arr2_indices = where(arange(len(arr2_indices)) < num_results, arr2_indices, arr2.size)
    if not assume_unique:
      arr1_indices = ind1.at[arr1_indices].get(mode='fill', fill_value=ind1.size)
      arr2_indices = ind2.at[arr2_indices].get(mode='fill', fill_value=ind2.size)
    return vals, arr1_indices, arr2_indices
  else:
    return vals

