
def _csr_fromdense(mat: Array, *, nse: int, index_dtype: DTypeLike = np.int32) -> tuple[Array, Array, Array]:
  """Create CSR-format sparse matrix from a dense matrix.

  Args:
    mat : array to be converted to CSR.
    nse : number of specified entries in ``mat``
    index_dtype : dtype of sparse indices

  Returns:
    data : array of shape ``(nse,)`` and dtype ``mat.dtype``.
    indices : array of shape ``(nse,)`` and dtype ``index_dtype``
    indptr : array of shape ``(mat.shape[0] + 1,)`` and dtype ``index_dtype``
  """
  mat = jnp.asarray(mat)
  nse = core.concrete_or_error(operator.index, nse, "nse argument of csr_fromdense()")
  return csr_fromdense_p.bind(mat, nse=nse, index_dtype=np.dtype(index_dtype))

