
def _coo_fromdense_impl(mat, *, nse, index_dtype):
  mat = jnp.asarray(mat)
  assert mat.ndim == 2

  row, col = jnp.nonzero(mat, size=nse)
  data = mat[row, col]

  true_nonzeros = jnp.arange(nse) < (mat != 0).sum()
  data = jnp.where(true_nonzeros, data, 0)

  return data, row.astype(index_dtype), col.astype(index_dtype)

