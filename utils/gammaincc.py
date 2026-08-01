
def gammaincc(a, x, dps=50, maxterms=10**8):
    """Compute gammaincc exactly like mpmath does but allow for more
    terms in hypercomb. See

    mpmath/functions/expintegrals.py#L187

    in the mpmath GitHub repository.

    """
    with mp.workdps(dps):
        z, a = a, x

        if mp.isint(z):
            try:
                # mpmath has a fast integer path
                return mpf2float(mp.gammainc(z, a=a, regularized=True))
            except mp.libmp.NoConvergence:
                pass
        nega = mp.fneg(a, exact=True)
        G = [z]
        # Use 2F0 series when possible; fall back to lower gamma representation
        try:
            def h(z):
                r = z-1
                return [([mp.exp(nega), a], [1, r], [], G, [1, -r], [], 1/nega)]
            return mpf2float(mp.hypercomb(h, [z], force_series=True))
        except mp.libmp.NoConvergence:
            def h(z):
                T1 = [], [1, z-1], [z], G, [], [], 0
                T2 = [-mp.exp(nega), a, z], [1, z, -1], [], G, [1], [1+z], a
                return T1, T2
            return mpf2float(mp.hypercomb(h, [z], maxterms=maxterms))


def gammaincc(a: ArrayLike, x: ArrayLike) -> Array:
  r"""The regularized upper incomplete gamma function.

  JAX implementation of :obj:`scipy.special.gammaincc`.

  .. math::

     \mathrm{gammaincc}(x; a) = \frac{1}{\Gamma(a)}\int_x^\infty t^{a-1}e^{-t}\mathrm{d}t

  where :math:`\Gamma(a)` is the :func:`~jax.scipy.special.gamma` function.

  Args:
    a: arraylike, real-valued. Positive shape parameter of the gamma distribution.
    x: arraylike, real-valued. Non-negative lower limit of integration

  Returns:
    array containing values of the gammaincc function.

  See Also:
    - :func:`jax.scipy.special.gamma`
    - :func:`jax.scipy.special.gammainc`
  """
  a, x = promote_args_inexact("gammaincc", a, x)
  return lax.igammac(a, x)

