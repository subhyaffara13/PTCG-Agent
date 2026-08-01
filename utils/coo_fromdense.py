
def coo_fromdense(mat: Array, *, nse: int | None = None, index_dtype: DTypeLike = jnp.int32) -> COO:
  """Create a COO-format sparse matrix from a dense matrix.

  Args:
    mat : array to be converted to COO.
    nse : number of specified entries in ``mat``. If not specified,
      it will be computed from the input matrix.
    index_dtype : dtype of sparse indices

  Returns:
    mat_coo : COO representation of the matrix.
  """
  if nse is None:
    nse = int((mat != 0).sum())
  nse_int = core.concrete_or_error(operator.index, nse, "coo_fromdense nse argument")
  return COO(_coo_fromdense(mat, nse=nse_int, index_dtype=index_dtype),
             shape=mat.shape, rows_sorted=True)

