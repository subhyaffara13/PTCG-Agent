
def roots_cubic(f, trig=False):
    """Returns a list of roots of a cubic polynomial.

    References
    ==========
    [1] https://en.wikipedia.org/wiki/Cubic_function, General formula for roots,
    (accessed November 17, 2014).
    """
    if trig:
        a, b, c, d = f.all_coeffs()
        p = (3*a*c - b**2)/(3*a**2)
        q = (2*b**3 - 9*a*b*c + 27*a**2*d)/(27*a**3)
        D = 18*a*b*c*d - 4*b**3*d + b**2*c**2 - 4*a*c**3 - 27*a**2*d**2
        if (D > 0) == True:
            rv = []
            for k in range(3):
                rv.append(2*sqrt(-p/3)*cos(acos(q/p*sqrt(-3/p)*Rational(3, 2))/3 - k*pi*Rational(2, 3)))
            return [i - b/3/a for i in rv]

    # a*x**3 + b*x**2 + c*x + d -> x**3 + a*x**2 + b*x + c
    _, a, b, c = f.monic().all_coeffs()

    if c is S.Zero:
        x1, x2 = roots([1, a, b], multiple=True)
        return [x1, S.Zero, x2]

    # x**3 + a*x**2 + b*x + c -> u**3 + p*u + q
    p = b - a**2/3
    q = c - a*b/3 + 2*a**3/27

    pon3 = p/3
    aon3 = a/3

    u1 = None
    if p is S.Zero:
        if q is S.Zero:
            return [-aon3]*3
        u1 = -root(q, 3) if q.is_positive else root(-q, 3)
    elif q is S.Zero:
        y1, y2 = roots([1, 0, p], multiple=True)
        return [tmp - aon3 for tmp in [y1, S.Zero, y2]]
    elif q.is_real and q.is_negative:
        u1 = -root(-q/2 + sqrt(q**2/4 + pon3**3), 3)

    coeff = I*sqrt(3)/2
    if u1 is None:
        u1 = S.One
        u2 = Rational(-1, 2) + coeff
        u3 = Rational(-1, 2) - coeff
        b, c, d = a, b, c  # a, b, c, d = S.One, a, b, c
        D0 = b**2 - 3*c  # b**2 - 3*a*c
        D1 = 2*b**3 - 9*b*c + 27*d  # 2*b**3 - 9*a*b*c + 27*a**2*d
        C = root((D1 + sqrt(D1**2 - 4*D0**3))/2, 3)
        return [-(b + uk*C + D0/C/uk)/3 for uk in [u1, u2, u3]]  # -(b + uk*C + D0/C/uk)/3/a

    u2 = u1*(Rational(-1, 2) + coeff)
    u3 = u1*(Rational(-1, 2) - coeff)

    if p is S.Zero:
        return [u1 - aon3, u2 - aon3, u3 - aon3]

    soln = [
        -u1 + pon3/u1 - aon3,
        -u2 + pon3/u2 - aon3,
        -u3 + pon3/u3 - aon3
    ]

    return soln

