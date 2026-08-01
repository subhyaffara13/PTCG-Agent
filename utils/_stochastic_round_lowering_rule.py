
def _stochastic_round_lowering_rule(
    ctx: LoweringRuleContext, x, random_bits, *, target_dtype
):
  if not isinstance(x.type.element_type, ir.F32Type):
    raise ValueError("Only float32 input is supported.")
  if target_dtype not in [
      jnp.bfloat16,
      jnp.float8_e5m2,
      jnp.float8_e4m3fn,
      jnp.float8_e4m3b11fnuz,
  ]:
    raise ValueError(
        "Only bfloat16, float8_e5m2, float8_e4m3fn, and float8_e4m3b11fnuz "
        "are supported as target dtypes."
    )
  (_, in_aval,) = ctx.avals_in
  out_type = ir.VectorType.get(
      ctx.lowering_context.dynamic_shape_replacement_fn(in_aval.shape),
      mlir.dtype_to_ir_type(jnp.dtype(target_dtype))
  )
  return tpu.stochastic_convert(out_type, x, random_bits)

