
def csr_matvec(mat: CSR, v: Array, transpose: bool = False) -> Array:
  """Product of CSR sparse matrix and a dense vector.

  Args:
    mat : CSR matrix
    v : one-dimensional array of size ``(shape[0] if transpose else shape[1],)`` and
      dtype ``mat.dtype``
    transpose : boolean specifying whether to transpose the sparse matrix
      before computing.

  Returns:
    y : array of shape ``(mat.shape[1] if transpose else mat.shape[0],)`` representing
      the matrix vector product.
  """
  data, indices, indptr = mat._bufs
  return _csr_matvec(data, indices, indptr, v, shape=mat.shape, transpose=transpose)

