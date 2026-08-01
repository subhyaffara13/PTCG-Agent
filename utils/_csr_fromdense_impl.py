
def _csr_fromdense_impl(mat, *, nse, index_dtype):
  mat = jnp.asarray(mat)
  assert mat.ndim == 2
  m = mat.shape[0]

  row, col = jnp.nonzero(mat, size=nse)
  data = mat[row, col]

  true_nonzeros = jnp.arange(nse) < (mat != 0).sum()
  data = jnp.where(true_nonzeros, data, 0)
  row = jnp.where(true_nonzeros, row, m)
  indices = col.astype(index_dtype)
  indptr = jnp.zeros(m + 1, dtype=index_dtype).at[1:].set(
      jnp.cumsum(jnp.bincount(row, length=m).astype(index_dtype)))
  return data, indices, indptr

