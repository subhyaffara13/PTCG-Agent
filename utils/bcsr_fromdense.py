
def bcsr_fromdense(mat: ArrayLike, *, nse: int | None = None, n_batch: int = 0,
                   n_dense:int = 0, index_dtype: DTypeLike = jnp.int32) -> BCSR:
  """Create BCSR-format sparse matrix from a dense matrix.

  Args:
    mat : array to be converted to BCOO.
    nse : number of stored elements in each batch
    n_batch : number of batch dimensions (default: 0)
    n_dense : number of dense dimensions (default: 0)
    index_dtype : dtype of sparse indices (default: int32)

  Returns:
    mat_bcsr: BCSR representation of the matrix.
  """
  mat_array = jnp.asarray(mat)
  nse_arr: int | Array | None = nse
  if nse_arr is None:
    nse_arr = _count_stored_elements(mat_array, n_batch, n_dense)
  nse_int: int = core.concrete_or_error(operator.index, nse_arr, _TRACED_NSE_ERROR)
  return BCSR(_bcsr_fromdense(mat_array, nse=nse_int, n_batch=n_batch,
                              n_dense=n_dense, index_dtype=index_dtype),
              shape=mat_array.shape)

