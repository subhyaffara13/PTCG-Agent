
def _svd_tpu_lowering_rule(
    ctx, operand, *, full_matrices, compute_uv, subset_by_index, algorithm=None
):
  operand_aval, = ctx.avals_in
  m, n = operand_aval.shape[-2:]

  if algorithm is not None and algorithm not in [
      lax_linalg.SvdAlgorithm.DEFAULT,
      lax_linalg.SvdAlgorithm.POLAR,
  ]:
    raise NotImplementedError(
        'Only the POLAR (which is also DEFAULT on TPU) SVD algorithm is'
        ' supported on TPU.'
    )

  if m == 0 or n == 0:
    return mlir.lower_fun(lax_linalg._empty_svd, multiple_results=True)(
        ctx,
        operand,
        full_matrices=full_matrices,
        compute_uv=compute_uv,
    )

  return mlir.lower_fun(_svd_tpu, multiple_results=True)(
      ctx,
      operand,
      full_matrices=full_matrices,
      compute_uv=compute_uv,
      subset_by_index=subset_by_index,
  )

