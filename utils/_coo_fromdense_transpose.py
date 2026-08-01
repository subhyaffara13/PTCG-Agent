
def _coo_fromdense_transpose(ct, M, *, nse, index_dtype):
  data, row, col = ct
  assert len(data) == nse
  assert row.dtype == col.dtype == index_dtype
  if isinstance(row, ad.Zero) or isinstance(col, ad.Zero):
    raise ValueError("Cannot transpose with respect to sparse indices")
  assert ad.is_undefined_primal(M)
  return _coo_todense(data, row, col, spinfo=COOInfo(shape=M.aval.shape))

