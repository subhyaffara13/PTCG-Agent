
def _hyp2f1_c_derivative(a, b, c, x):
  """
  Define it as a serie using :
  https://functions.wolfram.com/HypergeometricFunctions/Hypergeometric2F1/20/01/03/
  """

  precision = dtypes.finfo(x.dtype).eps

  def body(state):
    serie, k, term = state
    serie += term * (digamma(c) - digamma(c + k))
    term *= (a + k) * (b + k) / (c + k) / (k + 1) * x
    k += 1

    return serie, k, term

  def cond(state):
    serie, k, term = state

    return (k < 250) & (lax.abs(term) / lax.abs(serie) > precision)

  init = 0, 1, a * b / c * x

  return lax.while_loop(cond, body, init)[0]

