
def _csr_todense_transpose(ct, data, indices, indptr, *, shape):
  # Note: we assume that transpose has the same sparsity pattern.
  # Can we check this?
  assert ad.is_undefined_primal(data)
  if ad.is_undefined_primal(indices) or ad.is_undefined_primal(indptr):
    raise ValueError("Cannot transpose with respect to sparse indices")
  assert ct.shape == shape
  assert indices.aval.dtype == indptr.aval.dtype
  assert ct.dtype == data.aval.dtype
  return _csr_extract(indices, indptr, ct), indices, indptr

