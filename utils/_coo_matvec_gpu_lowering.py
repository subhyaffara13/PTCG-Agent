
def _coo_matvec_gpu_lowering(ctx, data, row, col, v, *, spinfo, transpose,
                             target_name_prefix):
  data_aval, row_aval, _, x_aval = ctx.avals_in
  dtype = data_aval.dtype
  if dtype not in [np.float32, np.float64, np.complex64, np.complex128]:
    warnings.warn(f"coo_matvec cusparse/hipsparse lowering not available for {dtype=}. "
                  "Falling back to default implementation.", CuSparseEfficiencyWarning)
    return _coo_matvec_lowering(ctx, data, row, col, v, spinfo=spinfo, transpose=transpose)

  if spinfo.rows_sorted:
    shape = spinfo.shape
  elif spinfo.cols_sorted:
    row, col = col, row
    transpose = not transpose
    shape = spinfo.shape[::-1]
  else:
    warnings.warn("coo_matvec GPU lowering requires matrices with sorted rows or sorted cols. "
                  "To sort the rows in your matrix, use e.g. mat = mat._sort_indices(). Falling "
                  "back to the default implementation.", CuSparseEfficiencyWarning)
    return _coo_matvec_lowering(ctx, data, row, col, v, spinfo=spinfo,
                                transpose=transpose)

  return _lowerings._coo_spmv_gpu_lowering(
      ctx, data, row, col, v, transpose=transpose, shape=shape,
      target_name_prefix=target_name_prefix)

