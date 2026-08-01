
def _eigh_tpu_lowering(
    ctx, operand, *, lower, sort_eigenvalues, subset_by_index, algorithm
):
  if algorithm is None:
    algorithm = lax_linalg.EighImplementation.QDWH

  if algorithm == lax_linalg.EighImplementation.QR:
    raise NotImplementedError("QR algorithm is not supported on TPU")

  elif algorithm == lax_linalg.EighImplementation.JACOBI:
    operand_aval, = ctx.avals_in
    if operand_aval.shape[-1] == 0:
      reshape_aval = operand_aval.update(shape=operand_aval.shape[:-1])
      return [
          operand,
          hlo.real(mlir.reshape(ctx, operand, reshape_aval)),
      ]

    v_aval, w_aval = ctx.avals_out
    eigvecs_type = mlir.aval_to_ir_type(ctx.module_context, v_aval)
    eigvals_type = mlir.aval_to_ir_type(ctx.module_context, w_aval)
    result_types = [eigvecs_type, eigvals_type]

    backend_config = f"{int(lower)},{int(sort_eigenvalues)},100,1e-6"

    if any(not is_constant_shape(aval_out.shape)
           for aval_out in ctx.avals_out):
      result_shapes = [
          mlir.eval_dynamic_shape_as_tensor(ctx, aval_out.shape)
          for aval_out in ctx.avals_out
      ]
    else:
      result_shapes = None
    op = mlir.custom_call(
        "Eigh",
        result_types=result_types,
        operands=[operand],
        backend_config=backend_config,
        api_version=1,
        result_shapes=result_shapes,
    )
    return op.results
  elif algorithm == lax_linalg.EighImplementation.QDWH:
    return mlir.lower_fun(_eigh_qdwh_impl, multiple_results=True)(
        ctx, operand, lower=lower, sort_eigenvalues=sort_eigenvalues,
        subset_by_index=subset_by_index)

  else:
    raise ValueError(f"Unknown algorithm: {algorithm}")

