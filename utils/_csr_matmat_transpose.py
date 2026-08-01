
def _csr_matmat_transpose(ct, data, indices, indptr, B, *, shape, transpose):
  assert not ad.is_undefined_primal(indices)
  assert not ad.is_undefined_primal(indptr)

  if ad.is_undefined_primal(B):
    return data, indices, indptr, _csr_matmat(data, indices, indptr, ct, shape=shape, transpose=not transpose)
  else:
    B = jnp.asarray(B)
    row, col = _csr_to_coo(indices, indptr)
    return (ct[row] * B[col]).sum(1), indices, indptr, B

