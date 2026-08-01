
def _bitcast_lowering_rule(ctx: LoweringRuleContext, x, *, ty):
  del ty
  (out_aval,) = ctx.avals_out
  return tpu.bitcast(ctx.aval_to_ir_type(out_aval), x)


def _bitcast_lowering_rule(ctx: mlir.LoweringRuleContext, x, *, ty):
  def _bitcast(x):
    src_bitwidth = dtypes.itemsize_bits(x.dtype)
    dst_bitwidth = dtypes.itemsize_bits(ty)
    if src_bitwidth < dst_bitwidth:
      *leading, m, n = x.shape
      packing = dst_bitwidth // src_bitwidth
      x = x.reshape(*leading, m // packing, packing, n)
      x = jnp.swapaxes(x, -1, -2)
      return jax.lax.bitcast_convert_type(x, ty)
    if src_bitwidth > dst_bitwidth:
      y = jax.lax.bitcast_convert_type(x, ty)
      *leading, m, n, packing = y.shape
      return jnp.swapaxes(y, -1, -2).reshape(*leading, m * packing, n)
    return jax.lax.bitcast_convert_type(x, ty)

  return mlir.lower_fun(_bitcast, multiple_results=False)(ctx, x)


def _bitcast_lowering_rule(ctx: sc_lowering.LoweringRuleContext, x, *, dtype):
  del dtype  # Unused.
  [out_aval] = ctx.avals_out
  return vector.bitcast(ctx.aval_to_ir_type(out_aval), x)

