
def _coo_matvec_impl(data, row, col, v, *, spinfo, transpose):
  v = jnp.asarray(v)
  if transpose:
    row, col = col, row
  out_shape = spinfo.shape[1] if transpose else spinfo.shape[0]
  dv = data * v[col]
  return jnp.zeros(out_shape, dv.dtype).at[row].add(dv)

