
def _odeint_fwd(func, rtol, atol, mxstep, hmax, y0, ts, *args):
  ys = _odeint(func, rtol, atol, mxstep, hmax, y0, ts, *args)
  return ys, (ys, ts, args)

