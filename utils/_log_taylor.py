from typing import Any

def _log_taylor(primals_in, series_in, **_):
  x, = primals_in
  series, = series_in
  u = [x] + series
  v: list[Any] = [lax.log(x)] + [None] * len(series)
  for k in range(1, len(v)):
    conv = sum(j * v[j] * u[k-j] for j in range(1, k))
    v[k] = (u[k] - conv / k) / u[0]
  primal_out, *series_out = v
  return primal_out, series_out

