
def csr_todense_gpu_lowering(ctx, data, indices, indptr, *, shape, target_name_prefix):
  data_aval, indices_aval, _, = ctx.avals_in
  nnz, = data_aval.shape
  rows, cols = shape
  buffer_size, opaque = _get_module(target_name_prefix).build_csr_todense_descriptor(
      data_aval.dtype, indices_aval.dtype, rows, cols, nnz)
  buffer_aval = core.ShapedArray(shape=(buffer_size,), dtype=np.int8)
  sub_ctx = ctx.replace(avals_out=[ctx.avals_out[0], buffer_aval])
  rule = ffi.ffi_lowering(f"{target_name_prefix}sparse_csr_todense_ffi")
  return rule(sub_ctx, data, indices, indptr, opaque=opaque)[0]

