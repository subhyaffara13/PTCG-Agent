
def _coo_spmm_gpu_lowering(ctx, data, row, col, x, *, transpose, shape,
                           target_name_prefix):
  data_aval, row_aval, _, x_aval = ctx.avals_in
  nnz, = data_aval.shape
  _, Ccols = x_aval.shape

  batch_count = 1
  if len(shape) == 2:
    rows, cols = shape
  elif len(shape) == 3:
    batch_count, rows, cols = shape
    nnz = nnz // batch_count
  else:
    raise NotImplementedError(f"Unsupported shape: {shape}")

  # TODO(tianjianlu): use batch stride to trigger different mode of batch
  # computation. Currently batch_stride = 0 is not allowed because of the issue
  # in cusparse https://github.com/NVIDIA/CUDALibrarySamples/issues/81#issuecomment-1205562643
  # Set batch stride to be the matrix size for now.
  lhs_batch_stride = nnz
  B_rows = rows if transpose else cols
  rhs_batch_stride =  B_rows * Ccols

  buffer_size, opaque = _get_module(target_name_prefix).build_coo_matmat_descriptor(
      data_aval.dtype, x_aval.dtype, data_aval.dtype, row_aval.dtype,
      rows, cols, Ccols, nnz, transpose, batch_count, lhs_batch_stride,
      rhs_batch_stride)

  buffer_aval = core.ShapedArray(shape=(buffer_size,), dtype=np.int8)
  sub_ctx = ctx.replace(avals_out=[ctx.avals_out[0], buffer_aval])
  rule = ffi.ffi_lowering(f"{target_name_prefix}sparse_coo_matmat_ffi")
  return rule(sub_ctx, data, row, col, x, opaque=opaque)[:1]

