
def diop_DN(D, N, t=symbols("t", integer=True)):
    """
    Solves the equation `x^2 - Dy^2 = N`.

    Explanation
    ===========

    Mainly concerned with the case `D > 0, D` is not a perfect square,
    which is the same as the generalized Pell equation. The LMM
    algorithm [1]_ is used to solve this equation.

    Returns one solution tuple, (`x, y)` for each class of the solutions.
    Other solutions of the class can be constructed according to the
    values of ``D`` and ``N``.

    Usage
    =====

    ``diop_DN(D, N, t)``: D and N are integers as in `x^2 - Dy^2 = N` and
    ``t`` is the parameter to be used in the solutions.

    Details
    =======

    ``D`` and ``N`` correspond to D and N in the equation.
    ``t`` is the parameter to be used in the solutions.

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import diop_DN
    >>> diop_DN(13, -4) # Solves equation x**2 - 13*y**2 = -4
    [(3, 1), (393, 109), (36, 10)]

    The output can be interpreted as follows: There are three fundamental
    solutions to the equation `x^2 - 13y^2 = -4` given by (3, 1), (393, 109)
    and (36, 10). Each tuple is in the form (x, y), i.e. solution (3, 1) means
    that `x = 3` and `y = 1`.

    >>> diop_DN(986, 1) # Solves equation x**2 - 986*y**2 = 1
    [(49299, 1570)]

    See Also
    ========

    find_DN(), diop_bf_DN()

    References
    ==========

    .. [1] Solving the generalized Pell equation x**2 - D*y**2 = N, John P.
        Robertson, July 31, 2004, Pages 16 - 17. [online], Available:
        https://web.archive.org/web/20160323033128/http://www.jpr2718.org/pell.pdf
    """
    if D < 0:
        if N == 0:
            return [(0, 0)]
        if N < 0:
            return []
        # N > 0:
        sol = []
        for d in divisors(square_factor(N), generator=True):
            for x, y in cornacchia(1, int(-D), int(N // d**2)):
                sol.append((d*x, d*y))
                if D == -1:
                    sol.append((d*y, d*x))
        return sol

    if D == 0:
        if N < 0:
            return []
        if N == 0:
            return [(0, t)]
        sN, _exact = integer_nthroot(N, 2)
        if _exact:
            return [(sN, t)]
        return []

    # D > 0
    sD, _exact = integer_nthroot(D, 2)
    if _exact:
        if N == 0:
            return [(sD*t, t)]

        sol = []
        for y in range(floor(sign(N)*(N - 1)/(2*sD)) + 1):
            try:
                sq, _exact = integer_nthroot(D*y**2 + N, 2)
            except ValueError:
                _exact = False
            if _exact:
                sol.append((sq, y))
        return sol

    if 1 < N**2 < D:
        # It is much faster to call `_special_diop_DN`.
        return _special_diop_DN(D, N)

    if N == 0:
        return [(0, 0)]

    sol = []
    if abs(N) == 1:
        pqa = PQa(0, 1, D)
        *_, prev_B, prev_G = next(pqa)
        for j, (*_, a, _, _B, _G) in enumerate(pqa):
            if a == 2*sD:
                break
            prev_B, prev_G = _B, _G
        if j % 2:
            if N == 1:
                sol.append((prev_G, prev_B))
            return sol
        if N == -1:
            return [(prev_G, prev_B)]
        for _ in range(j):
            *_, _B, _G = next(pqa)
        return [(_G, _B)]

    for f in divisors(square_factor(N), generator=True):
        m = N // f**2
        am = abs(m)
        for sqm in sqrt_mod(D, am, all_roots=True):
            z = symmetric_residue(sqm, am)
            pqa = PQa(z, am, D)
            *_, prev_B, prev_G = next(pqa)
            for _ in range(length(z, am, D) - 1):
                _, q, *_, _B, _G = next(pqa)
                if abs(q) == 1:
                    if prev_G**2 - D*prev_B**2 == m:
                        sol.append((f*prev_G, f*prev_B))
                    elif a := diop_DN(D, -1):
                        sol.append((f*(prev_G*a[0][0] + prev_B*D*a[0][1]),
                                    f*(prev_G*a[0][1] + prev_B*a[0][0])))
                    break
                prev_B, prev_G = _B, _G
    return sol

