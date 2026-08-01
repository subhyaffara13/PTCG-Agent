
def _pow_taylor(primals_in, series_in):
  u_, r_ = primals_in

  x, series = jet2(lambda x, y: lax.mul(y, lax.log(x)), primals_in, series_in)
  u = [x] + series
  v = [u_ ** r_] + [None] * len(series)
  for k in range(1, len(v)):
    v[k] = sum(j * v[k-j] * u[j] for j in range(1, k+1)) / k
  primal_out, *series_out = v

  return primal_out, series_out

