
def _coo_todense_transpose(ct, data, row, col, *, spinfo):
  # Note: we assume that transpose has the same sparsity pattern.
  # Can we check this?
  assert ad.is_undefined_primal(data)
  if ad.is_undefined_primal(row) or ad.is_undefined_primal(col):
    raise ValueError("Cannot transpose with respect to sparse indices")
  assert ct.shape == spinfo.shape
  assert row.aval.dtype == col.aval.dtype
  assert ct.dtype == data.aval.dtype
  return _coo_extract(row, col, ct), row, col

