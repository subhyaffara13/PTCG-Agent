
def _binary_op_lowering_rule_wg(
    ctx: LoweringRuleContext, x, y, *, ui_impl, si_impl, f_impl=None, **kwargs,
):
  if kwargs.get('out_dtype') is not None:
    raise NotImplementedError("out_dtype argument in binary_op_lowering_rule_wg")
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    if any(aval_in.shape for aval_in in ctx.avals_in):
      raise NotImplementedError(
          "Non-scalar arithmetic is not supported in warp-level lowering.")
  x_aval, y_aval = ctx.avals_in
  [out_aval] = ctx.avals_out
  x, y = _bcast_wg(x, y, *ctx.avals_in, *ctx.avals_out)
  if jnp.issubdtype(out_aval, jnp.signedinteger):
    return si_impl(x, y)
  elif jnp.issubdtype(out_aval, jnp.integer):
    return ui_impl(x, y)
  elif f_impl is not None and jnp.issubdtype(out_aval, jnp.floating):
    return f_impl(x, y)
  else:
    raise NotImplementedError(
        f"{ctx.prim} does not support {x_aval.dtype} and {y_aval.dtype}"
    )

