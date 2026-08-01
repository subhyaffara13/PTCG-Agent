
def _hyp2f1_serie(a, b, c, x):
  """
  Compute the 2F1 hypergeometric function using the Taylor expansion.
  See Eq. 4.1 from PEARSON, OLVER & PORTER 2014
  https://doi.org/10.48550/arXiv.1407.7786
  """
  rtol = dtypes.finfo(x.dtype).eps

  def body(state):
    serie, k, term = state

    serie += term
    term *= (a + k - 1) * (b + k - 1) / (c + k - 1) / k * x
    k += 1

    return serie, k, term

  def cond(state):
    serie, k, term = state

    return (k < 250) & (lax.abs(term) > rtol * lax.abs(serie))

  init = (jnp.array(0, dtype=x.dtype),
          jnp.array(1, dtype=x.dtype),
          jnp.array(1, dtype=x.dtype))

  return lax.while_loop(cond, body, init)[0]

