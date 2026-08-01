
def hyp2f1(ctx,a,b,c,z,**kwargs):
    return ctx.hyper([a,b],[c],z,**kwargs)


def hyp2f1(a: ArrayLike, b: ArrayLike, c: ArrayLike, x: ArrayLike) -> Array:
  r"""The 2F1 hypergeometric function.

  JAX implementation of :obj:`scipy.special.hyp2f1`.

  .. math::

     \mathrm{hyp2f1}(a, b, c, x) = {}_2F_1(a; b; c; x) = \sum_{k=0}^\infty \frac{(a)_k(b)_k}{(c)_k}\frac{x^k}{k!}

  where :math:`(\cdot)_k` is the Pochammer symbol.

  The JAX version only accepts positive and real inputs. Values of
  ``a``, ``b``, ``c``, and ``x`` leading to high values of 2F1 may
  lead to erroneous results; consider enabling double precision in this case.

  Args:
    a: arraylike, real-valued
    b: arraylike, real-valued
    c: arraylike, real-valued
    x: arraylike, real-valued

  Returns:
    array of 2F1 values.
  """
  # This is backed by https://doi.org/10.48550/arXiv.1407.7786
  a, b, c, x = promote_args_inexact('hyp2f1', a, b, c, x)
  eps = dtypes.finfo(x.dtype).eps * 50

  d = c - a - b
  s = 1 - x
  ca = c - a
  cb = c - b

  id = jnp.round(d)

  index = jnp.where(jnp.logical_or(x == 0, jnp.logical_and(jnp.logical_or(a == 0, b == 0), c != 0)), 0,
            jnp.where(jnp.logical_or(c == 0, jnp.logical_and(c < 0, c % 1 == 0)), 1,
              jnp.where(jnp.logical_and(d <= -1, jnp.logical_not(jnp.logical_and(jnp.abs(d - id) >= eps, s < 0))), 2,
                jnp.where(jnp.logical_and(d <= 0, x == 1), 1,
                  jnp.where(jnp.logical_and(x < 1, b == c), 3,
                    jnp.where(jnp.logical_and(x < 1, a == c), 4,
                      jnp.where(x > 1, 1,
                        jnp.where(x == 1, 5, 6))))))))

  return lax.select_n(index,
                      jnp.array(1, dtype=x.dtype),
                      jnp.array(np.inf, dtype=x.dtype),
                      s ** d * _hyp2f1_terminal_or_serie(ca, cb, c, x),
                      s ** (-a),
                      s ** (-b),
                      gamma(c) * gamma(d) / (gamma(ca) * gamma(cb)),
                      _hyp2f1_terminal_or_serie(a, b, c, x))

