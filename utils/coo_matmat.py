
def coo_matmat(mat: COO, B: Array, *, transpose: bool = False) -> Array:
  """Product of COO sparse matrix and a dense matrix.

  Args:
    mat : COO matrix
    B : array of shape ``(mat.shape[0] if transpose else mat.shape[1], cols)`` and
      dtype ``mat.dtype``
    transpose : boolean specifying whether to transpose the sparse matrix
      before computing.

  Returns:
    C : array of shape ``(mat.shape[1] if transpose else mat.shape[0], cols)``
      representing the matrix vector product.
  """
  data, row, col = mat._bufs
  return _coo_matmat(data, row, col, B, spinfo=mat._info, transpose=transpose)

