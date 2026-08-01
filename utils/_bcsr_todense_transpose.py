
def _bcsr_todense_transpose(ct, data, indices, indptr, *, spinfo):
  shape = spinfo.shape
  assert ad.is_undefined_primal(data)
  if ad.is_undefined_primal(indices) or ad.is_undefined_primal(indptr):
    raise ValueError("Cannot transpose with respect to sparse indices")
  assert ct.shape == shape
  assert ct.dtype == data.aval.dtype
  return bcsr_extract(indices, indptr, ct), indices, indptr

