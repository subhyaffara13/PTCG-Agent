
def deriv_prop(prim, deriv, primals_in, series_in):
  x, = primals_in
  series, = series_in
  primal_out = prim.bind(x)
  c0, cs = jet2(deriv, primals_in, series_in)
  c = [c0] + cs
  u = [x] + series
  v: list[Any] = [primal_out] + [None] * len(series)
  for k in range(1, len(v)):
    v[k] = sum(j * c[k-j] * u[j] for j in range(1, k + 1)) / k
  primal_out, *series_out = v
  return primal_out, series_out

