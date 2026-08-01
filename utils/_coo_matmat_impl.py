
def _coo_matmat_impl(data, row, col, B, *, spinfo, transpose):
  B = jnp.asarray(B)
  if transpose:
    row, col = col, row
  out_shape = spinfo.shape[1] if transpose else spinfo.shape[0]
  dB = data[:, None] * B[col]
  return jnp.zeros((out_shape, B.shape[1]), dB.dtype).at[row].add(dB)

