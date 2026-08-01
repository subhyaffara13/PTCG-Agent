
def _triangular_solve_cpu_lower(
    ctx, a, b, *, left_side, lower, transpose_a,
    conjugate_a, unit_diagonal):
  a_aval, b_aval = ctx.avals_in

  if conjugate_a and not transpose_a:
    a = chlo.conj(a)
    conjugate_a = False
  if np.dtype(a_aval.dtype) in _cpu_lapack_types:
    target_name = lapack.prepare_lapack_call("trsm_ffi", a_aval.dtype)
    alpha, alpha_aval, batch_partitionable = (), (), True
    rule = _linalg_ffi_lowering(target_name,
                                [a_aval, b_aval, *alpha_aval],
                                operand_output_aliases={1: 0},
                                batch_partitionable=batch_partitionable)
    return rule(ctx, a, b, *alpha,
                side=_matrix_side_attr(left_side),
                uplo=_matrix_uplo_attr(lower),
                trans_x=_matrix_transpose_attr(transpose_a, conjugate_a),
                diag=_matrix_diagonal_attr(unit_diagonal))
  else:
    # Fall back to the HLO implementation for unsupported types or batching.
    # TODO: Consider swapping XLA for LAPACK in batched case
    if transpose_a:
      transpose = "ADJOINT" if conjugate_a else "TRANSPOSE"
    else:
      transpose = "NO_TRANSPOSE"
    return [hlo.triangular_solve(a, b, ir.BoolAttr.get(left_side),
                                 ir.BoolAttr.get(lower),
                                 ir.BoolAttr.get(unit_diagonal),
                                 hlo.TransposeAttr.get(transpose))]

