
def _bcsr_todense(data: ArrayLike, indices: ArrayLike, indptr: ArrayLike, *,
                  spinfo: SparseInfo) -> Array:
  """Convert batched sparse matrix to a dense matrix.

  Args:
    data : array of shape ``batch_dims + (nse,) + dense_dims``.
    indices : array of shape ``batch_dims + (nse,)``.
    indptr : array of shape ``batch_dims + (shape[len(batch_dims)] + 1,).
    spinfo : SparseInfo. In particular, this includes the shape
      of the matrix, which is equal to
      ``batch_dims + 2(sparse_dims) + block_dims`` where
      ``len(sparse_dims) == 2``.
  Returns:
    mat : array with specified shape and dtype matching ``data``
  """
  return bcsr_todense_p.bind(jnp.asarray(data), jnp.asarray(indices),
                             jnp.asarray(indptr), spinfo=spinfo)

