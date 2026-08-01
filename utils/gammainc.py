
def gammainc(a, x, dps=50, maxterms=10**8):
    """Compute gammainc exactly like mpmath does but allow for more
    summands in hypercomb. See

    mpmath/functions/expintegrals.py#L134

    in the mpmath GitHub repository.

    """
    with mp.workdps(dps):
        z, a, b = mp.mpf(a), mp.mpf(x), mp.mpf(x)
        G = [z]
        negb = mp.fneg(b, exact=True)

        def h(z):
            T1 = [mp.exp(negb), b, z], [1, z, -1], [], G, [1], [1+z], b
            return (T1,)

        res = mp.hypercomb(h, [z], maxterms=maxterms)
        return mpf2float(res)


def gammainc(ctx, z, a=0, b=None, regularized=False):
    regularized = bool(regularized)
    z = ctx.convert(z)
    if a is None:
        a = ctx.zero
        lower_modified = False
    else:
        a = ctx.convert(a)
        lower_modified = a != ctx.zero
    if b is None:
        b = ctx.inf
        upper_modified = False
    else:
        b = ctx.convert(b)
        upper_modified = b != ctx.inf
    # Complete gamma function
    if not (upper_modified or lower_modified):
        if regularized:
            if ctx.re(z) < 0:
                return ctx.inf
            elif ctx.re(z) > 0:
                return ctx.one
            else:
                return ctx.nan
        return ctx.gamma(z)
    if a == b:
        return ctx.zero
    # Standardize
    if ctx.re(a) > ctx.re(b):
        return -ctx.gammainc(z, b, a, regularized)
    # Generalized gamma
    if upper_modified and lower_modified:
        return +ctx._gamma3(z, a, b, regularized)
    # Upper gamma
    elif lower_modified:
        return ctx._upper_gamma(z, a, regularized)
    # Lower gamma
    elif upper_modified:
        return ctx._lower_gamma(z, b, regularized)


def gammainc(a: ArrayLike, x: ArrayLike) -> Array:
  r"""The regularized lower incomplete gamma function.

  JAX implementation of :obj:`scipy.special.gammainc`.

  .. math::

     \mathrm{gammainc}(x; a) = \frac{1}{\Gamma(a)}\int_0^x t^{a-1}e^{-t}\mathrm{d}t

  where :math:`\Gamma(a)` is the :func:`~jax.scipy.special.gamma` function.

  Args:
    a: arraylike, real-valued. Positive shape parameter of the gamma distribution.
    x: arraylike, real-valued. Non-negative upper limit of integration

  Returns:
    array containing values of the gammainc function.

  See Also:
    - :func:`jax.scipy.special.gamma`
    - :func:`jax.scipy.special.gammaincc`
  """
  a, x = promote_args_inexact("gammainc", a, x)
  return lax.igamma(a, x)

