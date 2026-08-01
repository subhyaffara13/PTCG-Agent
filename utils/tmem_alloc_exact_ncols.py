
def tmem_alloc_exact_ncols(ncols: int, exact: bool) -> int:
  """Returns the exact number of columns to allocate in TMEM.

  The number of columns is rounded up to the nearest power of 2.

  Args:
    ncols: The number of columns to allocate.
    exact: If true, throws an error if the number of columns is not a power of 2
      and within [32, 512].
  """
  if exact:
    if ncols.bit_count() != 1 or not 32 <= ncols <= 512:
      raise ValueError(f"ncols must be a power of 2 and within [32, 512], got: {ncols}")
  else:
    ncols = max(32, 1 << (ncols - 1).bit_length())
    if ncols > 512:
      raise ValueError(
          f"After rounding up, got {ncols} columns, exceeding the limit of 512"
      )
  return ncols

