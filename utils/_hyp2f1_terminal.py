
def _hyp2f1_terminal(a, b, c, x):
  """
  The Taylor series representation of the 2F1 hypergeometric function
  terminates when either a or b is a non-positive integer. See Eq. 4.1 and
  Taylor Series Method (a) from PEARSON, OLVER & PORTER 2014
  https://doi.org/10.48550/arXiv.1407.7786
  """
  # Ensure that between a and b, the negative integer parameter with the greater
  # absolute value - that still has a magnitude less than the absolute value of
  # c if c is non-positive - is used for the upper limit in the loop.
  eps = dtypes.finfo(x.dtype).eps * 50
  ib = jnp.round(b)
  mask = jnp.logical_and(
      b < a,
      jnp.logical_and(
        jnp.abs(b - ib) < eps,
        jnp.logical_not(
          jnp.logical_and(
            c % 1 == 0,
            jnp.logical_and(
              c <= 0,
              c > b
            )
          )
        )
      )
    )
  orig_a = a
  a = jnp.where(mask, b, a)
  b = jnp.where(mask, orig_a, b)

  a = jnp.abs(a)

  def body(i, state):
    serie, term = state

    term *= -(a - i + 1) / (c + i - 1) * (b + i - 1) / i * x
    serie += term

    return serie, term

  init = (jnp.array(1, dtype=x.dtype), jnp.array(1, dtype=x.dtype))

  return lax.fori_loop(jnp.array(1, dtype=a.dtype),
                       a + 1,
                       body,
                       init)[0]

