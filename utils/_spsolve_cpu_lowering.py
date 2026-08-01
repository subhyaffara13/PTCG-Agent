
def _spsolve_cpu_lowering(ctx, data, indices, indptr, b, tol, reorder):
  del tol, reorder
  args = [data, indices, indptr, b]

  def _callback(data, indices, indptr, b, **kwargs):
    A = scipy.sparse.csr_matrix((data, indices, indptr), shape=(b.size, b.size))
    return (scipy.sparse.linalg.spsolve(A, b).astype(b.dtype),)

  result, _, _ = mlir.emit_python_callback(
      ctx, _callback, None, args, ctx.avals_in, ctx.avals_out,
      has_side_effect=False, returns_token=False)
  return result

