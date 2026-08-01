
def _igammac_continued_fraction(ax, x, a, enabled, dtype, mode):
  eps = dtypes.finfo(dtype).eps

  def cond_fn(vals):
    enabled, _ans, _t, _y, _x, c, *_ = vals
    return bitwise_and(c < _const(c, 2000), _any(enabled))

  def body_fn(vals):
    (enabled, ans, t, y, z, c, pkm1, qkm1, pkm2, qkm2,
       dpkm2_da, dqkm2_da, dpkm1_da, dqkm1_da, dans_da) = vals

    c = c + _const(c, 1)
    y = y + _const(y, 1)
    z = z + _const(z, 2)
    yc = y * c
    pk = pkm1 * z - pkm2 * yc
    qk = qkm1 * z - qkm2 * yc
    qk_is_nonzero = ne(qk, _const(qk, 0))
    r = pk / qk

    t = select(qk_is_nonzero, abs(div(sub(ans, r), r)), full_like(r, 1))
    ans = select(qk_is_nonzero, r, ans)

    dpk_da = dpkm1_da * z - pkm1 - dpkm2_da * yc + pkm2 * c
    dqk_da = dqkm1_da * z - qkm1 - dqkm2_da * yc + qkm2 * c
    dans_da_new = select(qk_is_nonzero, div(dpk_da - ans * dqk_da, qk), dans_da)
    grad_conditional = select(qk_is_nonzero,
                              abs(dans_da_new - dans_da),
                              full_like(dans_da, 1))

    pkm2 = pkm1
    pkm1 = pk
    qkm2 = qkm1
    qkm1 = qk

    dpkm2_da = dpkm1_da
    dqkm2_da = dqkm1_da
    dpkm1_da = dpk_da
    dqkm1_da = dqk_da

    rescale = gt(abs(pk), reciprocal(_const(pk, eps)))
    pkm2 = select(rescale, mul(pkm2, _const(pkm2, eps)), pkm2)
    pkm1 = select(rescale, mul(pkm1, _const(pkm1, eps)), pkm1)
    qkm2 = select(rescale, mul(qkm2, _const(qkm2, eps)), qkm2)
    qkm1 = select(rescale, mul(qkm1, _const(qkm1, eps)), qkm1)

    dpkm2_da = select(rescale, mul(dpkm2_da, _const(dpkm2_da, eps)), dpkm2_da)
    dqkm2_da = select(rescale, mul(dqkm2_da, _const(dqkm2_da, eps)), dqkm2_da)
    dpkm1_da = select(rescale, mul(dpkm1_da, _const(dpkm1_da, eps)), dpkm1_da)
    dqkm1_da = select(rescale, mul(dqkm1_da, _const(dqkm1_da, eps)), dqkm1_da)

    if mode == IgammaMode.VALUE:
      conditional = bitwise_and(enabled, t > eps)
    else:
      conditional = bitwise_and(enabled,
        grad_conditional > _const(grad_conditional, eps))

    return (conditional,
         select(enabled, ans, vals[1]),
         select(enabled, t, vals[2]),
         select(enabled, y, vals[3]),
         select(enabled, z, vals[4]),
         c,
         select(enabled, pkm1, vals[6]),
         select(enabled, qkm1, vals[7]),
         select(enabled, pkm2, vals[8]),
         select(enabled, qkm2, vals[9]),
         select(enabled, dpkm2_da, vals[10]),
         select(enabled, dqkm2_da, vals[11]),
         select(enabled, dpkm1_da, vals[12]),
         select(enabled, dqkm1_da, vals[13]),
         select(enabled, dans_da_new, vals[14]))

  y = _const(a, 1) - a
  z = x + y + _const(x, 1)
  c = _const(x, 0)
  pkm2 = full_like(x, 1)
  qkm2 = x
  pkm1 = x + _const(x, 1)
  qkm1 = z * x
  ans = pkm1 / qkm1
  t = full_like(x, 1)
  dpkm2_da = full_like(x, 0)
  dqkm2_da = full_like(x, 0)
  dpkm1_da = full_like(x, 0)
  dqkm1_da = -x
  dans_da = (dpkm1_da - ans * dqkm1_da) / qkm1
  init_vals = (enabled,  ans,    t,    y,    z,
               c,    pkm1,   qkm1,   pkm2,   qkm2,
               dpkm2_da, dqkm2_da, dpkm1_da, dqkm1_da, dans_da)

  vals = while_loop(cond_fn, body_fn, init_vals)
  ans = vals[1]
  if mode == IgammaMode.VALUE:
    return ans *  ax
  dans_da = vals[14]
  dlogax_da = log(x) -  digamma(a)

  if mode == IgammaMode.DERIVATIVE:
    return mul(ax, add(mul(ans, dlogax_da), dans_da))
  elif mode == IgammaMode.SAMPLE_DERIVATIVE:
    return neg(add(dans_da, mul(ans, dlogax_da)) * x)
  else:
    raise ValueError(f"Invalid mode: {mode}")

