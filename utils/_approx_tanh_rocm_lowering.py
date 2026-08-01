
def _approx_tanh_rocm_lowering(
    ctx: lowering.LoweringRuleContext,
    *args,
):
  """Lower approx_tanh for ROCm.

  AMD CDNA3 (MI300X/gfx942) does not have a hardware tanh instruction.
  See: https://github.com/triton-lang/triton/pull/7780
  """
  [arg] = args
  [out_aval] = ctx.avals_out
  in_dtype = ctx.avals_in[0].dtype

  if in_dtype == jnp.float64:
    result_type = mlir.aval_to_ir_type(ctx.context.mlir_ctx, out_aval)
    result = tt_dialect.extern_elementwise(
        result_type,
        list(args),
        libname="",
        libpath="",
        symbol="__ocml_tanh_f64",
        pure=True,
    )
    return [result]

  needs_cast = in_dtype in (jnp.float16, jnp.bfloat16)

  if needs_cast:
    f32_type = mlir.dtype_to_ir_type(jnp.dtype(jnp.float32))
    if out_aval.shape:
      result_type = ir.RankedTensorType.get(out_aval.shape, f32_type)
    else:
      result_type = f32_type
    arg = arith_dialect.extf(result_type, arg)
  else:
    result_type = mlir.aval_to_ir_type(ctx.context.mlir_ctx, out_aval)
  result = tt_dialect.extern_elementwise(
      result_type,
      [arg],
      libname="libdevice",
      libpath="",
      symbol="__triton_hip_fast_tanhf",
      pure=True,
  )

  if needs_cast:
    out_type = mlir.aval_to_ir_type(ctx.context.mlir_ctx, out_aval)
    result = arith_dialect.truncf(out_type, result)

  return [result]

