
def _log_ndtr_jvp(series_order, primals, tangents):
  (x,), (t,) = primals, tangents
  ans = log_ndtr(x, series_order=series_order)
  t_out = lax.mul(t, lax.exp(lax.sub(_norm_logpdf(x), ans)))
  return ans, t_out

