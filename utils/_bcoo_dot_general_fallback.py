
def _bcoo_dot_general_fallback(data, indices, spinfo):
  if data.dtype not in CUSPARSE_DATA_DTYPES:
    warnings.warn('bcoo_dot_general cusparse/hipsparse lowering not available '
                  f'for {data.dtype=}. Falling back to default implementation.',
                  CuSparseEfficiencyWarning)
    return True
  elif indices.dtype not in CUSPARSE_INDEX_DTYPES:
    warnings.warn('bcoo_dot_general cusparse/hipsparse lowering not available '
                  f'for {indices.dtype=}. Falling back to default implementation.',
                  CuSparseEfficiencyWarning)
    return True
  elif not spinfo.indices_sorted:
    warnings.warn("bcoo_dot_general GPU lowering requires matrices with "
                  "sorted indices. To sort the rows in your matrix, use e.g. "
                  "mat = mat.sort_indices(). Falling back to the default "
                  "implementation.", CuSparseEfficiencyWarning)
    return True
  else:
    return False

