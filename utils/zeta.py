
def zeta(s):
    """
    Riemann zeta function, real argument
    """
    if not isinstance(s, (float, int)):
        try:
            s = float(s)
        except (ValueError, TypeError):
            try:
                s = complex(s)
                if not s.imag:
                    return complex(zeta(s.real))
            except (ValueError, TypeError):
                pass
            raise NotImplementedError
    if s == 1:
        raise ValueError("zeta(1) pole")
    if s >= 27:
        return 1.0 + 2.0**(-s) + 3.0**(-s)
    n = int(s)
    if n == s:
        if n >= 0:
            return _zeta_int[n]
        if not (n % 2):
            return 0.0
    if s <= 0.0:
        return 2.**s*pi**(s-1)*_sinpi_real(0.5*s)*_gamma_real(1-s)*zeta(1-s)
    if s <= 2.0:
        if s <= 1.0:
            return _polyval(_zeta_0,s)/(s-1)
        return _polyval(_zeta_1,s)/(s-1)
    z = _polyval(_zeta_P,s) / _polyval(_zeta_Q,s)
    return 1.0 + 2.0**(-s) + 3.0**(-s) + 4.0**(-s)*z


def zeta(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.zeta(a, b)


def Zeta(name, s):
    r"""
    Create a discrete random variable with a Zeta distribution.

    Explanation
    ===========

    The density of the Zeta distribution is given by

    .. math::
        f(k) := \frac{1}{k^s \zeta{(s)}}

    Parameters
    ==========

    s : A value greater than 1

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Zeta, density, E, variance
    >>> from sympy import Symbol

    >>> s = 5
    >>> z = Symbol("z")

    >>> X = Zeta("x", s)

    >>> density(X)(z)
    1/(z**5*zeta(5))

    >>> E(X)
    pi**4/(90*zeta(5))

    >>> variance(X)
    -pi**8/(8100*zeta(5)**2) + zeta(3)/zeta(5)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Zeta_distribution

    """
    return rv(name, ZetaDistribution, s)


def zeta(x, q=None, out=None):
    r"""
    Riemann or Hurwitz zeta function.

    Parameters
    ----------
    x : array_like of float or complex
        Input data
    q : array_like of float, optional
        Input data, must be real.  Defaults to Riemann zeta. When `q` is
        ``None``, complex inputs `x` are supported. If `q` is not ``None``,
        then currently only real inputs `x` with ``x >= 1`` are supported,
        even when ``q = 1.0`` (corresponding to the Riemann zeta function).

    out : ndarray, optional
        Output array for the computed values.

    Returns
    -------
    out : array_like
        Values of zeta(x).

    See Also
    --------
    zetac

    Notes
    -----
    The two-argument version is the Hurwitz zeta function

    .. math::

        \zeta(x, q) = \sum_{k=0}^{\infty} \frac{1}{(k + q)^x};

    see [dlmf]_ for details. The Riemann zeta function corresponds to
    the case when ``q = 1``.

    For complex inputs with ``q = None``, points with
    ``abs(z.imag) > 1e9`` and ``0 <= abs(z.real) < 2.5`` are currently not
    supported due to slow convergence causing excessive runtime.

    References
    ----------
    .. [dlmf] NIST, Digital Library of Mathematical Functions,
        https://dlmf.nist.gov/25.11#i

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.special import zeta, polygamma, factorial

    Some specific values:

    >>> zeta(2), np.pi**2/6
    (1.6449340668482266, 1.6449340668482264)

    >>> zeta(4), np.pi**4/90
    (1.0823232337111381, 1.082323233711138)

    First nontrivial zero:

    >>> zeta(0.5 + 14.134725141734695j)
    0 + 0j

    Relation to the `polygamma` function:

    >>> m = 3
    >>> x = 1.25
    >>> polygamma(m, x)
    array(2.782144009188397)
    >>> (-1)**(m+1) * factorial(m) * zeta(m+1, x)
    2.7821440091883969

    """
    if q is None:
        return _ufuncs._riemann_zeta(x, out)
    else:
        return _ufuncs._zeta(x, q, out)


def zeta(ctx, s, a=1, derivative=0, method=None, **kwargs):
    d = int(derivative)
    if a == 1 and not (d or method):
        try:
            return ctx._zeta(s, **kwargs)
        except NotImplementedError:
            pass
    s = ctx.convert(s)
    prec = ctx.prec
    method = kwargs.get('method')
    verbose = kwargs.get('verbose')
    if (not s) and (not derivative):
        return ctx.mpf(0.5) - ctx._convert_param(a)[0]
    if a == 1 and method != 'euler-maclaurin':
        im = abs(ctx._im(s))
        re = abs(ctx._re(s))
        #if (im < prec or method == 'borwein') and not derivative:
        #    try:
        #        if verbose:
        #            print "zeta: Attempting to use the Borwein algorithm"
        #        return ctx._zeta(s, **kwargs)
        #    except NotImplementedError:
        #        if verbose:
        #            print "zeta: Could not use the Borwein algorithm"
        #        pass
        if abs(im) > 500*prec and 10*re < prec and derivative <= 4 or \
            method == 'riemann-siegel':
            try:   #  py2.4 compatible try block
                try:
                    if verbose:
                        print("zeta: Attempting to use the Riemann-Siegel algorithm")
                    return ctx.rs_zeta(s, derivative, **kwargs)
                except NotImplementedError:
                    if verbose:
                        print("zeta: Could not use the Riemann-Siegel algorithm")
                    pass
            finally:
                ctx.prec = prec
    if s == 1:
        return ctx.inf
    abss = abs(s)
    if abss == ctx.inf:
        if ctx.re(s) == ctx.inf:
            if d == 0:
                return ctx.one
            return ctx.zero
        return s*0
    elif ctx.isnan(abss):
        return 1/s
    if ctx.re(s) > 2*ctx.prec and a == 1 and not derivative:
        return ctx.one + ctx.power(2, -s)
    return +ctx._hurwitz(s, a, d, **kwargs)


def zeta(x: _ods_ir.Value, q: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ZetaOp(x=x, q=q, results=results, loc=loc, ip=ip).result


def zeta(x: ArrayLike, q: ArrayLike) -> Array:
  r"""Elementwise Hurwitz zeta function: :math:`\zeta(x, q)`"""
  x, q = core.auto_insert_reshard(x, q)
  return zeta_p.bind(x, q)


def zeta(x: ArrayLike, q: ArrayLike | None = None) -> Array:
  r"""The Hurwitz zeta function.

  JAX implementation of :func:`scipy.special.zeta`. JAX does not implement
  the Riemann zeta function (i.e. ``q = None``).

  .. math::

     \zeta(x, q) = \sum_{n=0}^\infty \frac{1}{(n + q)^x}

  Args:
    x: arraylike, real-valued
    q: arraylike, real-valued

  Returns:
    array of zeta function values
  """
  if q is None:
    raise NotImplementedError(
      "Riemann zeta function not implemented; pass q != None to compute the Hurwitz Zeta function.")
  x, q = promote_args_inexact("zeta", x, q)
  return lax.zeta(x, q)

