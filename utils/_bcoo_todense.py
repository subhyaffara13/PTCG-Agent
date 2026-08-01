
def _bcoo_todense(data: Array, indices: Array, *, spinfo: SparseInfo
                  ) -> Array:
  """Convert batched sparse matrix to a dense matrix.

  Args:
    data : array of shape ``batch_dims + (nse,) + block_dims``.
    indices : array of shape ``batch_dims + (n_sparse, nse)``
    spinfo : SparseInfo. In particular, this includes the shape
      of the matrix, which is equal to ``batch_dims + sparse_dims + block_dims``
      where ``len(sparse_dims) == n_sparse``

  Returns:
    mat : array with specified shape and dtype matching ``data``
  """
  return bcoo_todense_p.bind(jnp.asarray(data), jnp.asarray(indices), spinfo=spinfo)

