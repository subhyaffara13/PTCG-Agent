
def _tanh_taylor(primals_in, series_in, **_):
  x, = primals_in
  series, = series_in
  u = [2*x] + [2 * series_ for series_ in series]
  primals_in, *series_in = u
  primal_out, series_out = _logistic_taylor((primals_in, ), (series_in, ))
  series_out = [2 * series_ for series_ in series_out]
  return 2 * primal_out - 1, series_out

