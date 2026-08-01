
def _bcsr_fromdense_transpose(ct, M, *, nse, n_batch, n_dense, index_dtype):
  data, indices, indptr = ct
  n_sparse = M.ndim - n_batch - n_dense
  assert data.shape == M.shape[:n_batch] + (nse,) + M.shape[n_batch + n_sparse:]
  assert indices.shape == M.shape[:n_batch] + (n_sparse, nse)
  assert indptr.shape == M.shape[:n_batch] + (M.shape[n_batch] + 1,)
  assert indices.dtype == index_dtype
  assert indptr.dtype == index_dtype
  if isinstance(indices, ad.Zero) or isinstance(indptr, ad.Zero):
    raise ValueError("Cannot transpose with respect to sparse indices")
  assert ad.is_undefined_primal(M)
  return _bcsr_todense(data, indices, indptr, spinfo=SparseInfo(M.aval.shape))

