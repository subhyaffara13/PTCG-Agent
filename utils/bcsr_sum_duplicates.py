
def bcsr_sum_duplicates(mat: BCSR, nse: int | None = None) -> BCSR:
  """Sums duplicate indices within a BCSR array, returning an array with sorted indices.

  Args:
    mat : BCSR array
    nse : integer (optional). The number of specified elements in the output matrix. This must
      be specified for bcoo_sum_duplicates to be compatible with JIT and other JAX transformations.
      If not specified, the optimal nse will be computed based on the contents of the data and
      index arrays. If specified nse is larger than necessary, data and index arrays will be padded
      with standard fill values. If smaller than necessary, data elements will be dropped from the
      output matrix.

  Returns:
    mat_out : BCSR array with sorted indices and no duplicate indices.
  """
  return BCSR.from_bcoo(bcoo.bcoo_sum_duplicates(mat.to_bcoo(), nse=nse))

