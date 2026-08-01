
def _hyp1f1_asymptotic(a, b, x):
  """
  Compute the 1F1 hypergeometric function using asymptotic expansion
  See Eq. 3.8 and simplification for real inputs from PEARSON, OLVER & PORTER 2014
  https://doi.org/10.48550/arXiv.1407.7786
  """

  precision = dtypes.finfo(x.dtype).eps

  def body(state):
    serie, k, term = state
    serie += term
    term *= (b - a + k) * (1 - a + k) / (k + 1) / x
    k += 1

    return serie, k, term

  def cond(state):
    serie, k, term = state

    return (k < 250) & (lax.abs(term) / lax.abs(serie) > precision)

  init = 1, 1, (b - a) * (1 - a) / x
  serie = lax.while_loop(cond, body, init)[0]

  return gamma(b) / gamma(a) * lax.exp(x) * x ** (a - b) * serie

