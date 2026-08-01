
def test_solve_trig_hyp_symbolic():
    # actual solver: invert_trig_hyp
    assert dumeq(solveset(sin(a*x), x), ConditionSet(x, Ne(a, 0), Union(
        ImageSet(Lambda(n, (2*n*pi + pi)/a), S.Integers),
        ImageSet(Lambda(n, 2*n*pi/a), S.Integers))))

    assert dumeq(solveset(cosh(x/a), x), ConditionSet(x, Ne(a, 0), Union(
        ImageSet(Lambda(n, a*(2*n*I*pi + I*pi/2)), S.Integers),
        ImageSet(Lambda(n, a*(2*n*I*pi + 3*I*pi/2)), S.Integers))))

    assert dumeq(solveset(sin(2*sqrt(3)/3*a**2/(b*pi)*x)
        + cos(4*sqrt(3)/3*a**2/(b*pi)*x), x),
       ConditionSet(x, Ne(b, 0) & Ne(a**2, 0), Union(
           ImageSet(Lambda(n, sqrt(3)*pi*b*(2*n*pi + pi/2)/(2*a**2)), S.Integers),
           ImageSet(Lambda(n, sqrt(3)*pi*b*(2*n*pi - 5*pi/6)/(2*a**2)), S.Integers),
           ImageSet(Lambda(n, sqrt(3)*pi*b*(2*n*pi - pi/6)/(2*a**2)), S.Integers))))

    assert dumeq(solveset(cosh((a**2 + 1)*x) - 3, x), ConditionSet(
        x, Ne(a**2 + 1, 0), Union(
            ImageSet(Lambda(n, (2*n*I*pi - acosh(3))/(a**2 + 1)), S.Integers),
            ImageSet(Lambda(n, (2*n*I*pi + acosh(3))/(a**2 + 1)), S.Integers))))

    ar = Symbol('ar', real=True)
    assert solveset(cosh((ar**2 + 1)*x) - 2, x, S.Reals) == FiniteSet(
        -acosh(2)/(ar**2 + 1), acosh(2)/(ar**2 + 1))

    # actual solver: _solve_trig1
    assert dumeq(simplify(solveset(cot((1 + I)*x) - cot((3 + 3*I)*x), x)), Union(
        ImageSet(Lambda(n, pi*(1 - I)*(4*n + 1)/4), S.Integers),
        ImageSet(Lambda(n, pi*(1 - I)*(4*n - 1)/4), S.Integers)))

