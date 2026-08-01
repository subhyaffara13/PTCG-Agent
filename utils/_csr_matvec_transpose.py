
def _csr_matvec_transpose(ct, data, indices, indptr, v, *, shape, transpose):
  assert not ad.is_undefined_primal(indices)
  assert not ad.is_undefined_primal(indptr)

  if ad.is_undefined_primal(v):
    return data, indices, indptr, _csr_matvec(data, indices, indptr, ct, shape=shape, transpose=not transpose)
  else:
    v = jnp.asarray(v)
    # The following lines do this, but more efficiently.
    # return _csr_extract(indices, indptr, jnp.outer(ct, v)), indices, indptr, v
    row, col = _csr_to_coo(indices, indptr)
    return ct[row] * v[col], indices, indptr, v

