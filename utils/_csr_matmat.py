
def _csr_matmat(data: Array, indices: Array, indptr: Array, B: Array,
                *, shape: Shape, transpose: bool = False) -> Array:
  """Product of CSR sparse matrix and a dense matrix.

  Args:
    data : array of shape ``(nse,)``.
    indices : array of shape ``(nse,)``
    indptr : array of shape ``(shape[0] + 1,)`` and dtype ``indices.dtype``
    B : array of shape ``(shape[0] if transpose else shape[1], cols)`` and
      dtype ``data.dtype``
    shape : length-2 tuple representing the matrix shape
    transpose : boolean specifying whether to transpose the sparse matrix
      before computing.

  Returns:
    C : array of shape ``(shape[1] if transpose else shape[0], cols)``
      representing the matrix-matrix product.
  """
  return csr_matmat_p.bind(data, indices, indptr, B, shape=shape, transpose=transpose)

