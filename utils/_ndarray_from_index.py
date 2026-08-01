
def _ndarray_from_index(idx: Index) -> NpIndex:
  if idx:
    return np.stack([np_utils.int_tuple_from_slice(s) for s in idx])
  else:
    return np.empty([0, 3], dtype=int)

