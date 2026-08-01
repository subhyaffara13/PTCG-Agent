
def _bcsr_fromdense_impl(mat, *, nse, n_batch, n_dense, index_dtype):
  mat = jnp.asarray(mat)
  n_sparse = mat.ndim - n_dense - n_batch
  if n_sparse != 2:
    raise ValueError("bcsr_fromdense: must have 2 sparse dimensions.")
  bcoo_mat = bcoo.bcoo_fromdense(mat, nse=nse, index_dtype=index_dtype,
                                 n_dense=n_dense, n_batch=n_batch)
  indices, indptr = _bcoo_to_bcsr(
      bcoo_mat.indices, shape=mat.shape, index_dtype=index_dtype
  )
  return bcoo_mat.data, indices, indptr

