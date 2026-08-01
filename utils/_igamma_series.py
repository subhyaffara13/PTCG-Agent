
def _igamma_series(ax, x, a, enabled, dtype, mode):
  def cond_fn(vals):
    return _any(vals[0])

  def body_fn(vals):
    enabled, r, c, ans, x, dc_da, dans_da = vals

    r = r + _const(r, 1.)
    dc_da = dc_da * (x / r) - (c * x) / (r * r)
    dans_da = dans_da + dc_da
    c = c * (x / r)
    ans = ans + c

    if mode == IgammaMode.VALUE:
      conditional = bitwise_and(enabled, c / ans > dtypes.finfo(dtype).eps)
    else:
      conditional = bitwise_and(enabled,
                                abs(dc_da / dans_da) >  dtypes.finfo(dtype).eps)

    # TODO: Make this a vmap. Might be tricky with the imports.
    return (
      conditional,
      select(enabled, r, vals[1]),
      select(enabled, c, vals[2]),
      select(enabled, ans, vals[3]),
      select(enabled, x, vals[4]),
      select(enabled, dc_da, vals[5]),
      select(enabled, dans_da, vals[6]),
    )

  init_vals = (
    enabled, a, full_like(a, 1), full_like(a, 1), x, full_like(a, 0),
    full_like(a, 0),
  )

  vals = while_loop(cond_fn, body_fn, init_vals)
  ans = vals[3]
  dans_da = vals[6]

  if mode == IgammaMode.VALUE:
    return (ans * ax) / a

  dlogax_da = log(x) - digamma(a + _const(a, 1))

  if mode == IgammaMode.DERIVATIVE:
    return ax * (ans * dlogax_da + dans_da) / a
  elif mode == IgammaMode.SAMPLE_DERIVATIVE:
    return -(dans_da + ans * dlogax_da) * x / a
  else:
    raise ValueError("Invalid IgammaMode")

