
def _logistic_taylor(primals_in, series_in, **_):
  x, = primals_in
  series, = series_in
  u = [x] + series
  v: list[Any] = [lax.logistic(x)] + [None] * len(series)
  e: list[Any] = [v[0] * (1 - v[0])] + [None] * len(series)  # terms for sigmoid' = sigmoid * (1 - sigmoid)
  for k in range(1, len(v)):
    v[k] = sum(j * e[k-j] * u[j] for j in range(1, k+1)) / k
    e[k] = (1 - v[0]) * v[k] - sum(v[j] * v[k-j] for j in range(1, k+1))

  primal_out, *series_out = v
  return primal_out, series_out

