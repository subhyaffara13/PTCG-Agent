
def _div_taylor_rule(primals_in, series_in):
  x, y = primals_in
  x_terms, y_terms = series_in
  u = [x] + x_terms
  w = [y] + y_terms
  v = [None] * len(u)

  for k in range(0, len(v)):
    conv = sum(v[j] * w[k-j] for j in range(0, k))
    v[k] = (u[k] - conv) / w[0]
  primal_out, *series_out = v
  return primal_out, series_out

