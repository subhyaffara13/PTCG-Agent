
def _hyp2f1_digamma_transform(a, b, c, x):
  """
  Digamma transformation of the 2F1 hypergeometric function.
  See AMS55 #15.3.10, #15.3.11, #15.3.12
  """
  rtol = dtypes.finfo(x.dtype).eps

  d = c - a - b
  s = 1 - x
  rd = jnp.round(d)

  e = jnp.where(rd >= 0, d, -d)
  d1 = jnp.where(rd >= 0, d, jnp.array(0, dtype=d.dtype))
  d2 = jnp.where(rd >= 0, jnp.array(0, dtype=d.dtype), d)
  ard = jnp.where(rd >= 0, rd, -rd).astype('int32')

  ax = jnp.log(s)

  y = digamma(1.0) + digamma(1.0 + e) - digamma(a + d1) - digamma(b + d1) - ax
  y /= gamma(e + 1.0)

  p = (a + d1) * (b + d1) * s / gamma(e + 2.0)

  def cond(state):
    _, _, _, _, _, _, q, _, _, t, y = state

    return jnp.logical_and(
      t < 250,
      jnp.abs(q) >= rtol * jnp.abs(y)
    )

  def body(state):
    a, ax, b, d1, e, p, q, r, s, t, y = state

    r = digamma(1.0 + t) + digamma(1.0 + t + e) - digamma(a + t + d1) \
        - digamma(b + t + d1) - ax
    q = p * r
    y += q
    p *= s * (a + t + d1) / (t + 1.0)
    p *= (b + t + d1) / (t + 1.0 + e)
    t += 1.0

    return a, ax, b, d1, e, p, q, r, s, t, y

  init = (a, ax, b, d1, e, p, y, jnp.array(0, dtype=x.dtype), s,
          jnp.array(1, dtype=x.dtype), y)
  _, _, _, _, _, _, q, r, _, _, y = lax.while_loop(cond, body, init)

  def compute_sum(y):
    y1 = jnp.array(1, dtype=x.dtype)
    t = jnp.array(0, dtype=x.dtype)
    p = jnp.array(1, dtype=x.dtype)

    def for_body(i, state):
      a, b, d2, e, p, s, t, y1 = state

      r = 1.0 - e + t
      p *= s * (a + t + d2) * (b + t + d2) / r
      t += 1.0
      p /= t
      y1 += p

      return a, b, d2, e, p, s, t, y1

    init_val = a, b, d2, e, p, s, t, y1
    y1 = lax.fori_loop(1, ard, for_body, init_val)[-1]

    p = gamma(c)
    y1 *= gamma(e) * p / (gamma(a + d1) * gamma(b + d1))
    y *= p / (gamma(a + d2) * gamma(b + d2))

    y = jnp.where((ard & 1) != 0, -y, y)
    q = s ** rd

    return jnp.where(rd > 0, y * q + y1, y + y1 * q)

  return jnp.where(
    rd == 0,
    y * gamma(c) / (gamma(a) * gamma(b)),
    compute_sum(y)
  )

