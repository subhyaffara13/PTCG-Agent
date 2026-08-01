
def _gen_reduce_choose_taylor_rule(chooser_fun):
  def chooser_taylor_rule(primals_in, series_in, **params):
    operand, = primals_in
    gs, = series_in
    primal_out = chooser_fun(operand, **params)
    axes = params.pop("axes", None)
    primal_dtype = gs[0].dtype
    shape = [1 if i in axes else d for i, d in enumerate(operand.shape)]
    location_indicators = lax.convert_element_type(
        lax_internal._eq_meet(operand, lax.reshape(primal_out, shape)),
        primal_dtype)
    counts = lax.reduce_sum(location_indicators, axes)
    def _reduce_chooser_taylor_rule(g):
      return lax.div(
          lax.reduce_sum(lax.mul(g, location_indicators), axes),
          counts)
    series_out = [_reduce_chooser_taylor_rule(g) for g in gs]
    return primal_out, series_out
  return chooser_taylor_rule

