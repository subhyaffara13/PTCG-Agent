
def betainc(ctx, a, b, x1=0, x2=1, regularized=False):
    if x1 == x2:
        v = 0
    elif not x1:
        if x1 == 0 and x2 == 1:
            v = ctx.beta(a, b)
        else:
            v = x2**a * ctx.hyp2f1(a, 1-b, a+1, x2) / a
    else:
        m, d = ctx.nint_distance(a)
        if m <= 0:
            if d < -ctx.prec:
                h = +ctx.eps
                ctx.prec *= 2
                a += h
            elif d < -4:
                ctx.prec -= d
        s1 = x2**a * ctx.hyp2f1(a,1-b,a+1,x2)
        s2 = x1**a * ctx.hyp2f1(a,1-b,a+1,x1)
        v = (s1 - s2) / a
    if regularized:
        v /= ctx.beta(a,b)
    return v


def betainc(a, b, x): return scipy.special.betainc(a, b, x).astype(x.dtype)


def betainc(a: ArrayLike, b: ArrayLike, x: ArrayLike) -> Array:
  r"""Elementwise regularized incomplete beta integral."""
  a, b, x = core.auto_insert_reshard(a, b, x)
  return regularized_incomplete_beta_p.bind(a, b, x)


def betainc(a: ArrayLike, b: ArrayLike, x: ArrayLike) -> Array:
  r"""The regularized incomplete beta function.

  JAX implementation of :obj:`scipy.special.betainc`.

  .. math::

     \mathrm{betainc}(a, b, x) = \frac{1}{B(a, b)}\int_0^x t^{a-1}(1-t)^{b-1}\mathrm{d}t

  where :math:`B(a, b)` is the :func:`~jax.scipy.special.beta` function.

  Args:
    a: arraylike, real-valued. Parameter *a* of the beta distribution.
    b: arraylike, real-valued. Parameter *b* of the beta distribution.
    x: arraylike, real-valued. Upper limit of the integration.

  Returns:
    array containing values of the betainc function

  See Also:
    - :func:`jax.scipy.special.beta`
    - :func:`jax.scipy.special.betaln`
  """
  a, b, x = promote_args_inexact("betainc", a, b, x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    raise ValueError("betainc does not support complex-valued inputs.")
  return lax.betainc(a, b, x)

