
def bcoo_sum_duplicates(mat: BCOO, nse: int | None = None) -> BCOO:
  """Sums duplicate indices within a BCOO array, returning an array with sorted indices.

  Args:
    mat : BCOO array
    nse : integer (optional). The number of specified elements in the output matrix. This must
      be specified for bcoo_sum_duplicates to be compatible with JIT and other JAX transformations.
      If not specified, the optimal nse will be computed based on the contents of the data and
      index arrays. If specified nse is larger than necessary, data and index arrays will be padded
      with standard fill values. If smaller than necessary, data elements will be dropped from the
      output matrix.

  Returns:
    mat_out : BCOO array with sorted indices and no duplicate indices.
  """
  data, indices = _bcoo_sum_duplicates(mat.data, mat.indices, spinfo=mat._info, nse=nse)
  return BCOO((data, indices), shape=mat.shape, indices_sorted=True,
              unique_indices=True)

