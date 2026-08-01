
def bcoo_sort_indices(mat: BCOO) -> BCOO:
  """Sort indices of a BCOO array.

  Args:
    mat : BCOO array

  Returns:
    mat_out : BCOO array with sorted indices.
  """
  data, indices = bcoo_sort_indices_p.bind(*mat._bufs, spinfo=mat._info)
  return BCOO((data, indices), shape=mat.shape, indices_sorted=True,
              unique_indices=mat.unique_indices)

