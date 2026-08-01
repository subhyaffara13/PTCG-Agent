
def _bcoo_todense_transpose(ct, data, indices, *, spinfo):
  shape = spinfo.shape
  assert ad.is_undefined_primal(data)
  if ad.is_undefined_primal(indices):
    raise ValueError("Cannot transpose with respect to sparse indices")
  assert ct.shape == shape
  assert ct.dtype == data.aval.dtype
  return _bcoo_extract(indices, ct), indices

