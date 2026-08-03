from typing import Any

def _bilinear_taylor_rule(prim, primals_in, series_in, **params):
  x, y = primals_in
  x_terms, y_terms = series_in
  u = [x] + x_terms
  w = [y] + y_terms
  v: list[Any] = [None] * len(u)
  op = partial(prim.bind, **params)
  for k in range(0, len(v)):
    v[k] = sum(op(u[j], w[k-j]) for j in range(0, k+1))
  primal_out, *series_out = v
  return primal_out, series_out

