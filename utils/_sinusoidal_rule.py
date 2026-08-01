
def _sinusoidal_rule(sign, prims, primals_in, series_in, **_):
  x, = primals_in
  series, = series_in
  u = [x] + series
  s, c = prims
  s = [s(x)] + [None] * len(series)
  c = [c(x)] + [None] * len(series)
  for k in range(1, len(s)):
    s[k] = sum(j * u[j] * c[k-j] for j in range(1, k + 1)) / k
    c[k] = sum(j * u[j] * s[k-j] for j in range(1, k + 1)) / k * sign
  return (s[0], s[1:]), (c[0], c[1:])

