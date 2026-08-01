
def diop_bf_DN(D, N, t=symbols("t", integer=True)):
    r"""
    Uses brute force to solve the equation, `x^2 - Dy^2 = N`.

    Explanation
    ===========

    Mainly concerned with the generalized Pell equation which is the case when
    `D > 0, D` is not a perfect square. For more information on the case refer
    [1]_. Let `(t, u)` be the minimal positive solution of the equation
    `x^2 - Dy^2 = 1`. Then this method requires
    `\sqrt{\\frac{\mid N \mid (t \pm 1)}{2D}}` to be small.

    Usage
    =====

    ``diop_bf_DN(D, N, t)``: ``D`` and ``N`` are coefficients in
    `x^2 - Dy^2 = N` and ``t`` is the parameter to be used in the solutions.

    Details
    =======

    ``D`` and ``N`` correspond to D and N in the equation.
    ``t`` is the parameter to be used in the solutions.

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import diop_bf_DN
    >>> diop_bf_DN(13, -4)
    [(3, 1), (-3, 1), (36, 10)]
    >>> diop_bf_DN(986, 1)
    [(49299, 1570)]

    See Also
    ========

    diop_DN()

    References
    ==========

    .. [1] Solving the generalized Pell equation x**2 - D*y**2 = N, John P.
        Robertson, July 31, 2004, Page 15. https://web.archive.org/web/20160323033128/http://www.jpr2718.org/pell.pdf
    """
    D = as_int(D)
    N = as_int(N)

    sol = []
    a = diop_DN(D, 1)
    u = a[0][0]

    if N == 0:
        if D < 0:
            return [(0, 0)]
        if D == 0:
            return [(0, t)]
        sD, _exact = integer_nthroot(D, 2)
        if _exact:
            return [(sD*t, t), (-sD*t, t)]
        return [(0, 0)]

    if abs(N) == 1:
        return diop_DN(D, N)

    if N > 1:
        L1 = 0
        L2 = integer_nthroot(int(N*(u - 1)/(2*D)), 2)[0] + 1
    else: # N < -1
        L1, _exact = integer_nthroot(-int(N/D), 2)
        if not _exact:
            L1 += 1
        L2 = integer_nthroot(-int(N*(u + 1)/(2*D)), 2)[0] + 1

    for y in range(L1, L2):
        try:
            x, _exact = integer_nthroot(N + D*y**2, 2)
        except ValueError:
            _exact = False
        if _exact:
            sol.append((x, y))
            if not equivalent(x, y, -x, y, D, N):
                sol.append((-x, y))

    return sol

