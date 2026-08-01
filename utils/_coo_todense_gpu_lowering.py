
def _coo_todense_gpu_lowering(ctx, data, row, col, *, spinfo, target_name_prefix):
  data_aval, row_aval, _ = ctx.avals_in
  dtype = data_aval.dtype
  if not (np.issubdtype(dtype, np.floating) or np.issubdtype(dtype, np.complexfloating)):
    warnings.warn(f"coo_todense cusparse/hipsparse lowering not available for {dtype=}. "
                  "Falling back to default implementation.", CuSparseEfficiencyWarning)
    return _coo_todense_lowering(ctx, data, row, col, spinfo=spinfo)

  if spinfo.rows_sorted:
    shape = spinfo.shape
    transpose = False
  elif spinfo.cols_sorted:
    row, col = col, row
    transpose = True
    shape = spinfo.shape[::-1]
  else:
    warnings.warn("coo_todense GPU lowering requires matrices with sorted rows or sorted cols. "
                  "To sort the rows in your matrix, use e.g. mat = mat._sort_indices(). Falling "
                  "back to the default implementation.", CuSparseEfficiencyWarning)
    return _coo_todense_lowering(ctx, data, row, col, spinfo=spinfo)

  sub_ctx = ctx
  if transpose:
    out_aval, = ctx.avals_out
    out_aval = core.ShapedArray(shape=out_aval.shape[::-1], dtype=out_aval.dtype)
    sub_ctx = sub_ctx.replace(avals_out=[out_aval])
  result = _lowerings.coo_todense_gpu_lowering(
      sub_ctx, data, row, col, shape=shape, target_name_prefix=target_name_prefix)
  return (
      [hlo.transpose(result, mlir.dense_int_array([1, 0]))]
      if transpose else [result])

