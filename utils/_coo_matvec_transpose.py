
def _coo_matvec_transpose(ct, data, row, col, v, *, spinfo, transpose):
  assert not ad.is_undefined_primal(row)
  assert not ad.is_undefined_primal(col)

  if ad.is_undefined_primal(v):
    return data, row, col, _coo_matvec(data, row, col, ct, spinfo=spinfo, transpose=not transpose)
  else:
    v = jnp.asarray(v)
    # The following line does this, but more efficiently:
    # return _coo_extract(row, col, jnp.outer(ct, v)), row, col, v
    return ct[row] * v[col], row, col, v

