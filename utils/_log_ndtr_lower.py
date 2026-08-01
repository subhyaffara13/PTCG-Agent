
def _log_ndtr_lower(x, series_order):
  """Asymptotic expansion version of `Log[cdf(x)]`, appropriate for `x<<-1`."""
  dtype = lax.dtype(x).type
  x_2 = lax.square(x)
  # Log of the term multiplying (1 + sum)
  log_scale = -dtype(0.5) * x_2 - lax.log(-x) - dtype(0.5 * np.log(2. * np.pi))
  return log_scale + lax.log(_log_ndtr_asymptotic_series(x, series_order))

