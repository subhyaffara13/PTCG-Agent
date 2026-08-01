
def _hyp1f1_serie(a, b, x):
  """
  Compute the 1F1 hypergeometric function using the taylor expansion
  See Eq. 3.2 and associated method (a) from PEARSON, OLVER & PORTER 2014
  https://doi.org/10.48550/arXiv.1407.7786
  """

  precision = dtypes.finfo(x.dtype).eps

  def body(state):
    serie, k, term = state
    serie += term
    term *= (a + k) / (b + k) * x / (k + 1)
    k += 1

    return serie, k, term

  def cond(state):
    serie, k, term = state

    return (k < 250) & (lax.abs(term) / lax.abs(serie) > precision)

  init = 1, 1, a / b * x

  return lax.while_loop(cond, body, init)[0]

