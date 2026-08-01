
def _csr_fromdense_transpose(ct, M, *, nse, index_dtype):
  data, indices, indptr = ct
  assert len(data) == nse
  assert indices.dtype == indptr.dtype == index_dtype
  if isinstance(indices, ad.Zero) or isinstance(indptr, ad.Zero):
    raise ValueError("Cannot transpose with respect to sparse indices")
  assert ad.is_undefined_primal(M)
  return _csr_todense(data, indices, indptr, shape=M.aval.shape)

