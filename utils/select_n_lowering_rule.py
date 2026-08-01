
def select_n_lowering_rule(ctx: LoweringRuleContext, pred, x, y):
  pred_aval, a_aval, b_aval = ctx.avals_in
  [out_aval] = ctx.avals_out
  pred, x = _bcast(pred, x, pred_aval, a_aval, out_aval)
  pred, y = _bcast(pred, y, pred_aval, b_aval, out_aval)
  return arith_dialect.select(pred, y, x)

