
def _hyp1f1_b_derivative(a, b, x):
  """
  Define it as a serie using :
  https://functions.wolfram.com/HypergeometricFunctions/Hypergeometric1F1/20/01/02/
  """

  precision = dtypes.finfo(x.dtype).eps

  def body(state):
    serie, k, term = state
    serie += term * (digamma(b) - digamma(b + k))
    term *= (a + k) / (b + k) * x / (k + 1)
    k += 1

    return serie, k, term

  def cond(state):
    serie, k, term = state

    return (k < 250) & (lax.abs(term) / lax.abs(serie) > precision)

  init = 0, 1, a / b * x

  return lax.while_loop(cond, body, init)[0]

