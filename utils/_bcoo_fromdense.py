
def _bcoo_fromdense(mat: Array, *, nse: int, n_batch: int = 0, n_dense: int = 0,
                    index_dtype: DTypeLike = jnp.int32) -> tuple[Array, Array]:
  """Create BCOO-format sparse matrix from a dense matrix.

  Args:
    mat : array to be converted to BCOO, with ``ndim = n_batch + n_sparse + n_dense``.
    nse : number of specified elements in each batch
    n_batch : number of batch dimensions (default: 0)
    n_dense : number of block_dimensions (default: 0)
    index_dtype : dtype of sparse indices (default: int32)

  Returns:
    data : array of shape ``mat.shape[:n_batch] + (nse,) + mat.shape[mat.ndim - n_dense:]``
      and dtype ``mat.dtype``
    indices : array of shape ``mat.shape[:n_batch] + (n_sparse, nse)``
  """
  mat = jnp.asarray(mat)
  nse = core.concrete_or_error(operator.index, nse, _TRACED_NSE_ERROR)
  return bcoo_fromdense_p.bind(mat, nse=nse, n_batch=n_batch, n_dense=n_dense,
                               index_dtype=index_dtype)

