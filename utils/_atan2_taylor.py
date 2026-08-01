
def _atan2_taylor(primals_in, series_in):
  x, y = primals_in
  primal_out = lax.atan2(x, y)

  x, series = jet2(lax.div, primals_in, series_in)
  one = lax_internal._const(x, 1)
  c0, cs = jet2(lambda x: lax.div(one, 1 + lax.square(x)), (x, ), (series, ))
  c: list[Any] = [c0] + cs
  u: list[Any] = [x] + series
  v: list[Any] = [primal_out] + [None] * len(series)
  for k in range(1, len(v)):
    v[k] = sum(j * c[k-j] * u[j] for j in range(1, k + 1)) / k
  primal_out, *series_out = v
  return primal_out, series_out

