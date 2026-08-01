
def _convert_element_type_lowering_rule(
    ctx: LoweringRuleContext, x, *, new_dtype, weak_type, sharding
):
  del weak_type
  del sharding
  out_aval = ctx.avals_out[0]
  in_aval = ctx.avals_in[0]
  old_dtype = in_aval.dtype
  out_type = ctx.aval_to_ir_type(out_aval)

  if old_dtype == new_dtype:
    return x

  if new_dtype.itemsize == 8:
    raise NotImplementedError("64-bit types are not supported")

  _from = lambda dtype: jnp.issubdtype(old_dtype, dtype)
  _to = lambda dtype: jnp.issubdtype(new_dtype, dtype)
  floating = jnp.floating
  integer = jnp.integer
  signed = jnp.signedinteger
  unsigned = jnp.unsignedinteger
  old_bitwidth = dtypes.itemsize_bits(old_dtype)
  new_bitwidth = dtypes.itemsize_bits(new_dtype)
  if _from(floating) and _to(floating):
    if old_bitwidth < new_bitwidth:
      return arith.extf(out_type, x)
    elif old_bitwidth > new_bitwidth:
      return arith.truncf(out_type, x)
  elif _from(integer) and _to(integer):
    if old_bitwidth < new_bitwidth:
      if _from(unsigned):
        return arith.extui(out_type, x)
      if _from(signed):
        return arith.extsi(out_type, x)
    elif old_bitwidth > new_bitwidth:
      return arith.trunci(out_type, x)
    elif jnp.iinfo(old_dtype).bits == jnp.iinfo(new_dtype).bits:
      # This case triggers when casting signed to unsigned or vice versa.
      return x
  elif _from(floating) and _to(signed):
    return arith.fptosi(out_type, x)
  elif _from(signed) and _to(floating):
    return arith.sitofp(out_type, x)
  elif _from(floating) and _to(unsigned):
    return arith.fptoui(out_type, x)
  elif _from(unsigned) and _to(floating):
    return arith.uitofp(out_type, x)
  elif old_dtype == jnp.bool_ and _to(integer):
    # bool is either 0 or 1 in integer representation hence unsigned.
    return arith.extui(out_type, x)
  return lower_fun(functools.partial(_convert_helper, to_dtype=new_dtype))(
      ctx, x
  )


def _convert_element_type_lowering_rule(
    ctx: LoweringRuleContext, x, *, new_dtype, weak_type, sharding
):
  del weak_type, sharding
  [x_aval] = ctx.avals_in
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    if x_aval.shape != ():
      raise NotImplementedError(
          "Non-scalar arithmetic is not supported in warp-level lowering.")
  return _ensure_fa(x, x_aval.dtype).astype(
      mgpu_utils.dtype_to_ir_type(new_dtype), is_signed=mgpu_utils.is_signed(new_dtype)
  )


def _convert_element_type_lowering_rule(
    ctx: LoweringRuleContext, x, *, new_dtype, weak_type, sharding
):
  [x_aval] = ctx.avals_in
  x = _ensure_ir_value(x, x_aval)
  if new_dtype == x_aval.dtype:
    return x
  cc = ctx.context.compute_capability
  return _cast(x, x_aval.dtype, new_dtype, compute_capability=cc)

