
def _csr_spmv_gpu_lowering(ctx, data, indices, indptr, x, *, transpose, shape,
                           target_name_prefix):
  rows, cols = shape
  data_aval, indices_aval, _, x_aval = ctx.avals_in
  nnz, = data_aval.shape
  buffer_size, opaque = _get_module(target_name_prefix).build_csr_matvec_descriptor(
      data_aval.dtype, x_aval.dtype, data_aval.dtype, indices_aval.dtype,
      rows, cols, nnz, transpose)
  buffer_aval = core.ShapedArray(shape=(buffer_size,), dtype=np.int8)
  sub_ctx = ctx.replace(avals_out=[ctx.avals_out[0], buffer_aval])
  rule = ffi.ffi_lowering(f"{target_name_prefix}sparse_csr_matvec_ffi")
  return rule(sub_ctx, data, indices, indptr, x, opaque=opaque)[:1]

