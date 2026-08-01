
def _comparison_lowering_rule_wg(
    ctx: LoweringRuleContext, x, y, *, si_pred, ui_pred, f_pred
):
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    if any(aval_in.shape for aval_in in ctx.avals_in):
      raise NotImplementedError(
          "Non-scalar arithmetic is not supported in warp-level lowering.")
  x_aval, y_aval = ctx.avals_in
  x, y = _bcast_wg(x, y, *ctx.avals_in, *ctx.avals_out)
  if jnp.issubdtype(x_aval, jnp.signedinteger):
    return arith_dialect.cmpi(si_pred, x, y)
  elif jnp.issubdtype(x_aval, jnp.unsignedinteger) or jnp.issubdtype(x_aval, jnp.bool):
    return arith_dialect.cmpi(ui_pred, x, y)
  elif jnp.issubdtype(x_aval, jnp.floating):
    return arith_dialect.cmpf(f_pred, x, y)
  else:
    raise NotImplementedError(
        f"{ctx.prim} does not support {x_aval.dtype} and {y_aval.dtype}"
    )

