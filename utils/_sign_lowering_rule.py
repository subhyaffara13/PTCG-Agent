
def _sign_lowering_rule(ctx: LoweringRuleContext, x):
  (x_aval,) = ctx.avals_in
  dtype = x_aval.dtype
  tpu_gen = tpu_info.get_tpu_info().generation
  tpu_has_native_bf16 = tpu_gen >= 4

  def _lower_fun(x):
    if jnp.issubdtype(x.dtype, jnp.floating):
      # On modern TPUs, stay in 16-bit for bf16.
      if dtype == jnp.bfloat16 and tpu_has_native_bf16:
        ix = lax.bitcast_convert_type(x, jnp.uint16)
        sign_bit = lax.bitwise_and(ix, jnp.uint16(0x8000))
        sign_val_i = lax.bitwise_or(jnp.uint16(0x3F80), sign_bit)
        sign_val = lax.bitcast_convert_type(sign_val_i, jnp.bfloat16)
        # By checking abs(x) > 0.0 we handle NaN and +/-0.0.
        return jnp.where(jnp.abs(x) > 0.0, sign_val, x)

      # f32 path for f32 inputs or older TPUs.
      x32 = x.astype(jnp.float32)
      ix = lax.bitcast_convert_type(x32, jnp.uint32)
      sign_bit = lax.bitwise_and(ix, jnp.uint32(0x80000000))
      sign_val_i = lax.bitwise_or(jnp.uint32(0x3F800000), sign_bit)
      sign_val = lax.bitcast_convert_type(sign_val_i, jnp.float32)
      # By checking abs(x32) > 0.0 we handle NaN and +/-0.0.
      res = jnp.where(jnp.abs(x32) > 0.0, sign_val, x32)

      if dtype == jnp.bfloat16:
        assert not tpu_has_native_bf16
        # Drop the rightmost 16 bits, which are all zero.
        res_i = lax.bitcast_convert_type(res, jnp.uint32)
        res_u16 = lax.convert_element_type(
            lax.shift_right_logical(res_i, jnp.uint32(16)), jnp.uint16
        )
        return lax.bitcast_convert_type(res_u16, jnp.bfloat16)
      return res.astype(dtype)

    if jnp.issubdtype(x.dtype, jnp.signedinteger):
      return (x > 0).astype(x.dtype) - (x < 0).astype(x.dtype)
    if jnp.issubdtype(x.dtype, jnp.unsignedinteger):
      return (x != 0).astype(x.dtype)
    raise ValueError(f"Unsupported dtype for sign: {x.dtype}")

  return lower_fun(_lower_fun)(ctx, x)


def _sign_lowering_rule(ctx: LoweringRuleContext, x):
  def sign(x):
    if jnp.issubdtype(x.dtype, jnp.floating):
      ones = lax.full(x.shape, 1.0, dtype=x.dtype)
      zeros = lax.full(x.shape, 0.0, dtype=x.dtype)
      return lax.select(x != 0, _copysign(ones, x), zeros)
    if jnp.issubdtype(x.dtype, jnp.signedinteger):
      return (x > 0).astype(x.dtype) - (x < 0).astype(x.dtype)
    if jnp.issubdtype(x.dtype, jnp.unsignedinteger):
      return (x != 0).astype(x.dtype)
    raise ValueError(f"Unsupported dtype for sign: {x.dtype}")

  return _lower_fun(sign)(ctx, x)

