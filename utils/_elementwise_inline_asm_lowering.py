
def _elementwise_inline_asm_lowering(
    ctx: lowering.LoweringRuleContext,
    *args,
    asm,
    constraints,
    pack,
    result_shape_dtypes,
):
  del result_shape_dtypes  # Unused.

  if "tanh.approx" in asm:
    if ctx.context.platform == "rocm":
      return _approx_tanh_rocm_lowering(ctx, *args)
    if ctx.avals_in[0].dtype == jnp.float64:
      raise TypeError(
          "approx_tanh does not support float64 on CUDA; it is only"
          " supported on ROCm"
      )

  return [
      tt_dialect.elementwise_inline_asm(
          [mlir.aval_to_ir_type(ctx.context.mlir_ctx, aval) for aval in ctx.avals_out],
          asm,
          constraints=constraints,
          pure=True,
          packed_element=pack,
          args=args,
      )
  ]

