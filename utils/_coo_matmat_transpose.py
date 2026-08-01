
def _coo_matmat_transpose(ct, data, row, col, B, *, spinfo, transpose):
  assert not ad.is_undefined_primal(row)
  assert not ad.is_undefined_primal(col)
  if ad.is_undefined_primal(B):
    return data, row, col, _coo_matmat(data, row, col, ct, spinfo=spinfo, transpose=not transpose)
  else:
    B = jnp.asarray(B)
    return (ct[row] * B[col]).sum(1), row, col, B

