
def _bcoo_extract_transpose(ct, indices, arr, *, assume_unique):
  if not assume_unique:
    raise NotImplementedError("transpose of bcoo_extract with assume_unique=False")
  assert ad.is_undefined_primal(arr)
  if ad.is_undefined_primal(indices):
    raise ValueError("Cannot transpose with respect to sparse indices")
  assert ct.dtype == arr.aval.dtype
  return indices, _bcoo_todense(ct, indices, spinfo=SparseInfo(arr.aval.shape))

