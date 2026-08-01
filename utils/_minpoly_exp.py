
def _minpoly_exp(ex, x):
    """
    Returns the minimal polynomial of ``exp(ex)``
    """
    c, a = ex.args[0].as_coeff_Mul()
    if a == I*pi:
        if c.is_rational:
            q = sympify(c.q)
            if c.p == 1 or c.p == -1:
                if q == 3:
                    return x**2 - x + 1
                if q == 4:
                    return x**4 + 1
                if q == 6:
                    return x**4 - x**2 + 1
                if q == 8:
                    return x**8 + 1
                if q == 9:
                    return x**6 - x**3 + 1
                if q == 10:
                    return x**8 - x**6 + x**4 - x**2 + 1
                if q.is_prime:
                    s = 0
                    for i in range(q):
                        s += (-x)**i
                    return s

            # x**(2*q) = product(factors)
            factors = [cyclotomic_poly(i, x) for i in divisors(2*q)]
            mp = _choose_factor(factors, x, ex)
            return mp
        else:
            raise NotAlgebraic("%s does not seem to be an algebraic element" % ex)
    raise NotAlgebraic("%s does not seem to be an algebraic element" % ex)

