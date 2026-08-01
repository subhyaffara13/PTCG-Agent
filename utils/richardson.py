
def richardson(A, k, n, N):
    """
    Calculate an approximation for lim k->oo A(k) using Richardson
    extrapolation with the terms A(n), A(n+1), ..., A(n+N+1).
    Choosing N ~= 2*n often gives good results.

    Examples
    ========

    A simple example is to calculate exp(1) using the limit definition.
    This limit converges slowly; n = 100 only produces two accurate
    digits:

        >>> from sympy.abc import n
        >>> e = (1 + 1/n)**n
        >>> print(round(e.subs(n, 100).evalf(), 10))
        2.7048138294

    Richardson extrapolation with 11 appropriately chosen terms gives
    a value that is accurate to the indicated precision:

        >>> from sympy import E
        >>> from sympy.series.acceleration import richardson
        >>> print(round(richardson(e, n, 10, 20).evalf(), 10))
        2.7182818285
        >>> print(round(E.evalf(), 10))
        2.7182818285

    Another useful application is to speed up convergence of series.
    Computing 100 terms of the zeta(2) series 1/k**2 yields only
    two accurate digits:

        >>> from sympy.abc import k, n
        >>> from sympy import Sum
        >>> A = Sum(k**-2, (k, 1, n))
        >>> print(round(A.subs(n, 100).evalf(), 10))
        1.6349839002

    Richardson extrapolation performs much better:

        >>> from sympy import pi
        >>> print(round(richardson(A, n, 10, 20).evalf(), 10))
        1.6449340668
        >>> print(round(((pi**2)/6).evalf(), 10))     # Exact value
        1.6449340668

    """
    s = S.Zero
    for j in range(0, N + 1):
        s += (A.subs(k, Integer(n + j)).doit() * (n + j)**N *
              S.NegativeOne**(j + N) / (factorial(j) * factorial(N - j)))
    return s


def richardson(ctx, seq):
    r"""
    Given a list ``seq`` of the first `N` elements of a slowly convergent
    infinite sequence, :func:`~mpmath.richardson` computes the `N`-term
    Richardson extrapolate for the limit.

    :func:`~mpmath.richardson` returns `(v, c)` where `v` is the estimated
    limit and `c` is the magnitude of the largest weight used during the
    computation. The weight provides an estimate of the precision
    lost to cancellation. Due to cancellation effects, the sequence must
    be typically be computed at a much higher precision than the target
    accuracy of the extrapolation.

    **Applicability and issues**

    The `N`-step Richardson extrapolation algorithm used by
    :func:`~mpmath.richardson` is described in [1].

    Richardson extrapolation only works for a specific type of sequence,
    namely one converging like partial sums of
    `P(1)/Q(1) + P(2)/Q(2) + \ldots` where `P` and `Q` are polynomials.
    When the sequence does not convergence at such a rate
    :func:`~mpmath.richardson` generally produces garbage.

    Richardson extrapolation has the advantage of being fast: the `N`-term
    extrapolate requires only `O(N)` arithmetic operations, and usually
    produces an estimate that is accurate to `O(N)` digits. Contrast with
    the Shanks transformation (see :func:`~mpmath.shanks`), which requires
    `O(N^2)` operations.

    :func:`~mpmath.richardson` is unable to produce an estimate for the
    approximation error. One way to estimate the error is to perform
    two extrapolations with slightly different `N` and comparing the
    results.

    Richardson extrapolation does not work for oscillating sequences.
    As a simple workaround, :func:`~mpmath.richardson` detects if the last
    three elements do not differ monotonically, and in that case
    applies extrapolation only to the even-index elements.

    **Example**

    Applying Richardson extrapolation to the Leibniz series for `\pi`::

        >>> from mpmath import *
        >>> mp.dps = 30; mp.pretty = True
        >>> S = [4*sum(mpf(-1)**n/(2*n+1) for n in range(m))
        ...     for m in range(1,30)]
        >>> v, c = richardson(S[:10])
        >>> v
        3.2126984126984126984126984127
        >>> nprint([v-pi, c])
        [0.0711058, 2.0]

        >>> v, c = richardson(S[:30])
        >>> v
        3.14159265468624052829954206226
        >>> nprint([v-pi, c])
        [1.09645e-9, 20833.3]

    **References**

    1. [BenderOrszag]_ pp. 375-376

    """
    if len(seq) < 3:
        raise ValueError("seq should be of minimum length 3")
    if ctx.sign(seq[-1]-seq[-2]) != ctx.sign(seq[-2]-seq[-3]):
        seq = seq[::2]
    N = len(seq)//2-1
    s = ctx.zero
    # The general weight is c[k] = (N+k)**N * (-1)**(k+N) / k! / (N-k)!
    # To avoid repeated factorials, we simplify the quotient
    # of successive weights to obtain a recurrence relation
    c = (-1)**N * N**N / ctx.mpf(ctx._ifac(N))
    maxc = 1
    for k in xrange(N+1):
        s += c * seq[N+k]
        maxc = max(abs(c), maxc)
        c *= (k-N)*ctx.mpf(k+N+1)**N
        c /= ((1+k)*ctx.mpf(k+N)**N)
    return s, maxc

