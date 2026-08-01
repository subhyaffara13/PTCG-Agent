
def csr_matmat(mat: CSR, B: Array, *, transpose: bool = False) -> Array:
  """Product of CSR sparse matrix and a dense matrix.

  Args:
    mat : CSR matrix
    B : array of shape ``(mat.shape[0] if transpose else mat.shape[1], cols)`` and
      dtype ``mat.dtype``
    transpose : boolean specifying whether to transpose the sparse matrix
      before computing.

  Returns:
    C : array of shape ``(mat.shape[1] if transpose else mat.shape[0], cols)``
      representing the matrix vector product.
  """
  data, indices, indptr = mat._bufs
  return _csr_matmat(data, indices, indptr, B, shape=mat.shape, transpose=transpose)

