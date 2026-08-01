
def _spsolve_transpose(ct, data, indices, indptr, b, **kwds):
  assert not ad.is_undefined_primal(indices)
  assert not ad.is_undefined_primal(indptr)
  if ad.is_undefined_primal(b):
    # TODO(jakevdp): can we do this without an explicit transpose?
    data_T, indices_T, indptr_T = _csr_transpose(data, indices, indptr)
    ct_out = spsolve(data_T, indices_T, indptr_T, ct, **kwds)
    return data, indices, indptr, ct_out
  else:
    # Should never reach here, because JVP is linear wrt data.
    raise NotImplementedError("spsolve transpose with respect to data")

