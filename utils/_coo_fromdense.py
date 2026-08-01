
def _coo_fromdense(mat: Array, *, nse: int, index_dtype: DTypeLike = jnp.int32) -> tuple[Array, Array, Array]:
  """Create COO-format sparse matrix from a dense matrix.

  Args:
    mat : array to be converted to COO.
    nse : number of specified entries in ``mat``
    index_dtype : dtype of sparse indices

  Returns:
    data : array of shape ``(nse,)`` and dtype ``mat.dtype``
    row : array of shape ``(nse,)`` and dtype ``index_dtype``
    col : array of shape ``(nse,)`` and dtype ``index_dtype``
  """
  mat = jnp.asarray(mat)
  nse = core.concrete_or_error(operator.index, nse, "nse argument of coo_fromdense()")
  return coo_fromdense_p.bind(mat, nse=nse, index_dtype=index_dtype)

