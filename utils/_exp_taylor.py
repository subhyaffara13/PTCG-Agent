from typing import Any

def _exp_taylor(primals_in, series_in, **_):
  x, = primals_in
  series, = series_in
  u = [x] + series
  v: list[Any] = [lax.exp(x)] + [None] * len(series)
  for k in range(1,len(v)):
    v[k] = sum(j * v[k-j] * u[j] for j in range(1, k+1)) / k
  primal_out, *series_out = v
  return primal_out, series_out

