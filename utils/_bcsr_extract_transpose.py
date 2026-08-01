
def _bcsr_extract_transpose(ct, indices, indptr, arr):
  assert ad.is_undefined_primal(arr)
  if ad.is_undefined_primal(indices) or ad.is_undefined_primal(indptr):
    raise ValueError("Cannot transpose with respect to sparse indices")
  assert ct.dtype == arr.aval.dtype
  return indices, indptr, _bcsr_todense(ct, indices, indptr, spinfo=SparseInfo(arr.aval.shape))

