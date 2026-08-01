
def _setxor1d_size(arr1: Array, arr2: Array, fill_value: ArrayLike | None, *,
                   assume_unique: bool, size: int, ) -> Array:
  # Ensured by caller
  assert arr1.ndim == arr2.ndim == 1
  assert arr1.dtype == arr2.dtype

  if assume_unique:
    arr = concatenate([arr1, arr2])
    aux = sort(concatenate([arr1, arr2]))
    flag = concatenate((bool(aux.size), aux[1:] != aux[:-1], True), axis=None)
  else:
    arr, num_unique = _concat_unique(arr1, arr2)
    mask = arange(arr.size + 1) < num_unique + 1
    _, aux = lax.sort([~mask[1:], arr], is_stable=True, num_keys=2)
    flag = mask & concatenate((bool(aux.size), aux[1:] != aux[:-1], False),
                              axis=None).at[num_unique].set(True)
  aux_mask = flag[1:] & flag[:-1]
  num_results = aux_mask.sum()
  if aux.size:
    indices = nonzero(aux_mask, size=size, fill_value=len(aux))[0]
    vals = aux.at[indices].get(mode='fill', fill_value=0)
  else:
    vals = zeros(size, aux.dtype)
  if fill_value is None:
    vals = where(arange(len(vals)) < num_results, vals, vals.max())
    return where(arange(len(vals)) < num_results, vals, vals.min())
  else:
    return where(arange(len(vals)) < num_results, vals, fill_value)

