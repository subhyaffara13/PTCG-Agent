
def bcoo_reduce_sum(mat: BCOO, *, axes: Sequence[int]) -> BCOO:
  """Sum array element over given axes.

  Args:
    mat: A BCOO-format array.
    shape: The shape of the target array.
    axes:  A tuple or list or ndarray which contains axes of ``mat`` over which
      sum is performed.

  Returns:
    A BCOO-format array containing the result.
  """
  out_data, out_indices, out_shape = _bcoo_reduce_sum(
      mat.data, mat.indices, spinfo=mat._info, axes=axes)
  return BCOO((out_data, out_indices), shape=out_shape)

