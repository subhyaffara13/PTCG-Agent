
def _in1d(ar1: ArrayLike, ar2: ArrayLike, invert: bool,
          method='auto', assume_unique=False) -> Array:
  ar1, ar2 = ensure_arraylike("in1d", ar1, ar2)
  arr1, arr2 = promote_dtypes(ar1, ar2)
  arr1, arr2 = arr1.ravel(), arr2.ravel()
  if arr1.size == 0 or arr2.size == 0:
    return (ones if invert else zeros)(arr1.shape, dtype=bool)
  if method in ['auto', 'compare_all']:
    if invert:
      return (arr1[:, None] != arr2[None, :]).all(-1)
    else:
      return (arr1[:, None] == arr2[None, :]).any(-1)
  elif method == 'binary_search':
    from jax._src.numpy.lax_numpy import searchsorted

    arr2 = lax.sort(arr2)
    ind = searchsorted(arr2, arr1)
    if invert:
      return arr1 != arr2[ind]
    else:
      return arr1 == arr2[ind]
  elif method == 'sort':
    if assume_unique:
      ind_out: slice | Array = slice(None)
    else:
      arr1, ind_out = unique(arr1, size=len(arr1), return_inverse=True, fill_value=arr2.max())
    aux, ind = lax.sort_key_val(concatenate([arr1, arr2]), arange(arr1.size + arr2.size))
    if invert:
      return ones(arr1.shape, bool).at[ind[:-1]].set(aux[1:] != aux[:-1], mode='drop')[ind_out]
    else:
      return zeros(arr1.shape, bool).at[ind[:-1]].set(aux[1:] == aux[:-1], mode='drop')[ind_out]
  else:
    raise ValueError(f"{method=} is not implemented; options are "
                     "'compare_all', 'binary_search', 'sort', and 'auto'")

