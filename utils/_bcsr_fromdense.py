
def _bcsr_fromdense(mat: ArrayLike, *, nse: int, n_batch: int = 0, n_dense: int = 0,
                    index_dtype: DTypeLike = jnp.int32) -> tuple[Array, Array, Array]:
  """Create BCSR-format sparse matrix from a dense matrix.

  Args:
    mat : array to be converted to BCSR, with
      ``ndim = n_batch + n_sparse + n_dense``.
    nse : number of stored elements in each batch.
    n_batch : number of batch dimensions (default: 0)
    n_dense : number of dense dimensions (default: 0)
    index_dtype : dtype of sparse indices (default: int32)

  Returns:
    data : array of shape
    ``mat.shape[:n_batch] + (nse,) + mat.shape[mat.ndim - n_dense:]``
      and dtype ``mat.dtype``
    indices : array of shape ``mat.shape[:n_batch] + (nse,)`` and dtype of
      ``index_type``.
    indptr: array of shape ``mat.shape[:n_batch] + (mat.shape[n_batch] + 1,)``
      and dtype of ``index_type``.
  """
  mat = jnp.asarray(mat)
  nse = core.concrete_or_error(operator.index, nse, _TRACED_NSE_ERROR)
  return bcsr_fromdense_p.bind(mat, nse=nse, n_batch=n_batch, n_dense=n_dense,
                               index_dtype=index_dtype)

