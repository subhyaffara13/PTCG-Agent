
def _select_n_lowering_rule(ctx: LoweringRuleContext, pred, x, *args):
  if len(args) > 1:
    raise NotImplementedError("select_n only supported with <= 2 arguments")
  pred_aval, x_aval = ctx.avals_in[:2]
  if pred_aval.dtype != np.dtype(np.bool_):
    lower_ctx = LoweringRuleContext(
        ctx.lowering_context,
        avals_in=[pred_aval],
        avals_out=[pred_aval.update(dtype=np.bool_)],
        block_shapes=[None],
    )
    pred = lower_fun(lambda x: x != 0)(lower_ctx, pred)
  if not args:
    return x
  # Assume x and y, which we check above.
  y, = args
  return arith.select(pred, y, x)


def _select_n_lowering_rule(ctx: LoweringRuleContext, pred, *cases):
  if len(cases) != 2:
    raise NotImplementedError(
        "Mosaic GPU lowering only supports select_n with 2 cases, got"
        f" {len(cases)}"
    )
  pred_aval, *cases_avals = ctx.avals_in
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    if not all(aval.shape == () for aval in ctx.avals_in):
      raise NotImplementedError(
          "Can only select on scalars in warp-level lowering.")
  [out_aval] = ctx.avals_out
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    pred = _ensure_fa(pred, pred_aval.dtype)
    cases = _bcast(*cases, *cases_avals, out_aval=out_aval)
    # ``select`` expects the first case to be the true branch, but ``select_n``
    # orders the cases in reverse.
    return pred.select(*reversed(cases))
  else:
    pred = _ensure_ir_value(pred, pred_aval.dtype)
    cases = [_ensure_ir_value(c, c_aval.dtype) for c, c_aval in zip(cases, cases_avals)]
    # TODO(bchetioui): support implicit broadcast.
    if any(a.shape != out_aval.shape for a in ctx.avals_in):
      raise NotImplementedError(
          "Implicit broadcast not implemented with warpgroup semantics")
    # ``select`` expects the first case to be the true branch, but ``select_n``
    # orders the cases in reverse.
    return arith_dialect.select(pred, *reversed(cases))

