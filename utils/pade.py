
def pade(an, m, n=None):
    """
    Return Pade approximation to a polynomial as the ratio of two polynomials.

    .. deprecated:: 1.18.0
        This function is deprecated and will be removed in SciPy 1.20.0. Use
        `mpmath.pade` instead.

    Parameters
    ----------
    an : (N,) array_like
        Taylor series coefficients.
    m : int
        The order of the returned approximating polynomial `q`.
    n : int, optional
        The order of the returned approximating polynomial `p`. By default,
        the order is ``len(an)-1-m``.

    Returns
    -------
    p, q : Polynomial class
        The Pade approximation of the polynomial defined by `an` is
        ``p(x)/q(x)``.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.interpolate import pade
    >>> e_exp = [1.0, 1.0, 1.0/2.0, 1.0/6.0, 1.0/24.0, 1.0/120.0]
    >>> p, q = pade(e_exp, 2)

    >>> e_exp.reverse()
    >>> e_poly = np.poly1d(e_exp)

    Compare ``e_poly(x)`` and the Pade approximation ``p(x)/q(x)``

    >>> e_poly(1)
    2.7166666666666668

    >>> p(1)/q(1)
    2.7179487179487181

    """
    _warn_skips = (os.path.dirname(__file__),)
    msg = ("`pade` is deprecated and will be removed in SciPy 1.20.0. Use "
           "`mpmath.pade` instead.")
    warnings.warn(msg, DeprecationWarning, skip_file_prefixes=_warn_skips)
    an = asarray(an)
    if n is None:
        n = len(an) - 1 - m
        if n < 0:
            raise ValueError("Order of q <m> must be smaller than len(an)-1.")
    if n < 0:
        raise ValueError("Order of p <n> must be greater than 0.")
    N = m + n
    if N > len(an)-1:
        raise ValueError("Order of q+p <m+n> must be smaller than len(an).")
    an = an[:N+1]
    Akj = eye(N+1, n+1, dtype=an.dtype)
    Bkj = zeros((N+1, m), dtype=an.dtype)
    for row in range(1, m+1):
        Bkj[row,:row] = -(an[:row])[::-1]
    for row in range(m+1, N+1):
        Bkj[row,:] = -(an[row-m:row])[::-1]
    C = hstack((Akj, Bkj))
    pq = linalg.solve(C, an)
    p = pq[:n+1]
    q = r_[1.0, pq[n+1:]]
    return poly1d(p[::-1]), poly1d(q[::-1])


def pade(ctx, a, L, M):
    r"""
    Computes a Pade approximation of degree `(L, M)` to a function.
    Given at least `L+M+1` Taylor coefficients `a` approximating
    a function `A(x)`, :func:`~mpmath.pade` returns coefficients of
    polynomials `P, Q` satisfying

    .. math ::

        P = \sum_{k=0}^L p_k x^k

        Q = \sum_{k=0}^M q_k x^k

        Q_0 = 1

        A(x) Q(x) = P(x) + O(x^{L+M+1})

    `P(x)/Q(x)` can provide a good approximation to an analytic function
    beyond the radius of convergence of its Taylor series (example
    from G.A. Baker 'Essentials of Pade Approximants' Academic Press,
    Ch.1A)::

        >>> from mpmath import *
        >>> mp.dps = 15; mp.pretty = True
        >>> one = mpf(1)
        >>> def f(x):
        ...     return sqrt((one + 2*x)/(one + x))
        ...
        >>> a = taylor(f, 0, 6)
        >>> p, q = pade(a, 3, 3)
        >>> x = 10
        >>> polyval(p[::-1], x)/polyval(q[::-1], x)
        1.38169105566806
        >>> f(x)
        1.38169855941551

    """
    # To determine L+1 coefficients of P and M coefficients of Q
    # L+M+1 coefficients of A must be provided
    if len(a) < L+M+1:
        raise ValueError("L+M+1 Coefficients should be provided")

    if M == 0:
        if L == 0:
            return [ctx.one], [ctx.one]
        else:
            return a[:L+1], [ctx.one]

    # Solve first
    # a[L]*q[1] + ... + a[L-M+1]*q[M] = -a[L+1]
    # ...
    # a[L+M-1]*q[1] + ... + a[L]*q[M] = -a[L+M]
    A = ctx.matrix(M)
    for j in range(M):
        for i in range(min(M, L+j+1)):
            A[j, i] = a[L+j-i]
    v = -ctx.matrix(a[(L+1):(L+M+1)])
    x = ctx.lu_solve(A, v)
    q = [ctx.one] + list(x)
    # compute p
    p = [0]*(L+1)
    for i in range(L+1):
        s = a[i]
        for j in range(1, min(M,i) + 1):
            s += q[j]*a[i-j]
        p[i] = s
    return p, q

