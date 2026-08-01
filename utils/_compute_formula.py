
def _compute_formula(f, x, P, Q, k, m, k_max):
    """Computes the formula for f."""
    from sympy.polys import roots

    sol = []
    for i in range(k_max + 1, k_max + m + 1):
        if (i < 0) == True:
            continue
        r = f.diff(x, i).limit(x, 0) / factorial(i)
        if r.is_zero:
            continue

        kterm = m*k + i
        res = r

        p = P.subs(k, kterm)
        q = Q.subs(k, kterm)
        c1 = p.subs(k, 1/k).leadterm(k)[0]
        c2 = q.subs(k, 1/k).leadterm(k)[0]
        res *= (-c1 / c2)**k

        res *= Mul(*[rf(-r, k)**mul for r, mul in roots(p, k).items()])
        res /= Mul(*[rf(-r, k)**mul for r, mul in roots(q, k).items()])

        sol.append((res, kterm))

    return sol

