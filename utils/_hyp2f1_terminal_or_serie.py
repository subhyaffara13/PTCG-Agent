
def _hyp2f1_terminal_or_serie(a, b, c, x):
  """
  Check for recurrence relations along with whether or not the series
  terminates. True recursion is not possible; however, the recurrence
  relation may still be approximated.
  See 4.6.1. Recurrence Relations from PEARSON, OLVER & PORTER 2014
  https://doi.org/10.48550/arXiv.1407.7786
  """
  eps = dtypes.finfo(x.dtype).eps * 50

  d = c - a - b

  ia = jnp.round(a)
  ib = jnp.round(b)
  id = jnp.round(d)

  neg_int_a = jnp.logical_and(a <= 0, jnp.abs(a - ia) < eps)
  neg_int_b = jnp.logical_and(b <= 0, jnp.abs(b - ib) < eps)
  neg_int_a_or_b = jnp.logical_or(neg_int_a, neg_int_b)
  not_neg_int_a_or_b = jnp.logical_not(neg_int_a_or_b)

  index = jnp.where(jnp.logical_and(x > 0.9, not_neg_int_a_or_b),
        jnp.where(jnp.abs(d - id) >= eps, 0, 1),
        jnp.where(neg_int_a_or_b, 2, 0))

  return lax.select_n(index,
                      _hyp2f1_serie(a, b, c, x),
                      _hyp2f1_digamma_transform(a, b, c, x),
                      _hyp2f1_terminal(a, b, c, x))

