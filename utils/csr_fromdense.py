
def csr_fromdense(mat: Array, *, nse: int | None = None, index_dtype: DTypeLike = np.int32) -> CSR:
  """Create a CSR-format sparse matrix from a dense matrix.

  Args:
    mat : array to be converted to CSR.
    nse : number of specified entries in ``mat``. If not specified,
      it will be computed from the input matrix.
    index_dtype : dtype of sparse indices

  Returns:
    mat_coo : CSR representation of the matrix.
  """
  if nse is None:
    nse = int((mat != 0).sum())
  nse_int = core.concrete_or_error(operator.index, nse, "coo_fromdense nse argument")
  return CSR(_csr_fromdense(mat, nse=nse_int, index_dtype=index_dtype), shape=mat.shape)

