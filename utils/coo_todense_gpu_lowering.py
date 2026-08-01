
def coo_todense_gpu_lowering(ctx, data, row, col, *, shape, target_name_prefix):
  data_aval, row_aval, _ = ctx.avals_in
  nnz, = data_aval.shape
  rows, cols = shape
  buffer_size, opaque = _get_module(target_name_prefix).build_coo_todense_descriptor(
      data_aval.dtype, row_aval.dtype, rows, cols, nnz)
  buffer_aval = core.ShapedArray(shape=(buffer_size,), dtype=np.int8)
  sub_ctx = ctx.replace(avals_out=[ctx.avals_out[0], buffer_aval])
  rule = ffi.ffi_lowering(f"{target_name_prefix}sparse_coo_todense_ffi")
  return rule(sub_ctx, data, row, col, opaque=opaque)[0]

