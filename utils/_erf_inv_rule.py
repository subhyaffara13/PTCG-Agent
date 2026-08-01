
def _erf_inv_rule(primals_in, series_in):
  x, = primals_in
  series, = series_in

  u: list[Any] = [x] + series
  primal_out = lax.erf_inv(x)
  v: list[Any] = [primal_out] + [None] * len(series)

  # derivative on co-domain for caching purposes
  deriv_const = np.sqrt(np.pi) / 2.
  deriv_y = lambda y: lax.mul(deriv_const, lax.exp(lax.square(y)))

  # manually propagate through deriv_y since we don't have lazy evaluation of sensitivities

  c: list[Any] = [deriv_y(primal_out)] + [None] * (len(series) - 1)
  tmp_sq: list[Any] = [lax.square(v[0])] + [None] * (len(series) - 1)
  tmp_exp: list[Any] = [lax.exp(tmp_sq[0])] + [None] * (len(series) - 1)
  for k in range(1, len(series)):
    # we know c[:k], we compute c[k]

    # propagate c to get v
    v[k] = sum(j * c[k-j] * u[j] for j in range(1, k + 1)) / k

    # propagate v to get next c

    # square
    tmp_sq[k] = sum( v[k-j] * v[j] for j in range(k + 1))

    # exp
    tmp_exp[k] = sum(j * tmp_exp[k-j] * tmp_sq[j] for j in range(1, k + 1)) / k

    # const
    c[k] = deriv_const * tmp_exp[k]

  # we can't, and don't need, to compute c[k+1], just need to get the last v[k]
  k = len(series)
  v[k] = sum(j * c[k-j] * u[j] for j in range(1, k + 1)) / k

  primal_out, *series_out = v
  return primal_out, series_out

