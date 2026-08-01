
def bcoo_multiply_dense(sp_mat: BCOO, v: Array) -> Array:
  """An element-wise multiplication between a sparse and a dense array.

  Args:
    lhs: A BCOO-format array.
    rhs: An ndarray.

  Returns:
    An ndarray containing the result.
  """
  return _bcoo_multiply_dense(sp_mat.data, sp_mat.indices, v, spinfo=sp_mat._info)

