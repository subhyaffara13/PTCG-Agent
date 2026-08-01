
def _spsolve_gpu_lowering(ctx, data, indices, indptr, b, *, tol, reorder):
  return ffi.ffi_lowering("cusolver_csrlsvqr_ffi")(
      ctx, data, indices, indptr, b, tol=np.float64(tol),
      reorder=np.int32(reorder))

