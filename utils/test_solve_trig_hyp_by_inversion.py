
def test_solve_trig_hyp_by_inversion():
    n = Dummy('n')
    assert solveset_real(sin(2*x + 3) - S(1)/2, x).dummy_eq(Union(
        ImageSet(Lambda(n, n*pi - S(3)/2 + 13*pi/12), S.Integers),
        ImageSet(Lambda(n, n*pi - S(3)/2 + 17*pi/12), S.Integers)))
    assert solveset_complex(sin(2*x + 3) - S(1)/2, x).dummy_eq(Union(
        ImageSet(Lambda(n, n*pi - S(3)/2 + 13*pi/12), S.Integers),
        ImageSet(Lambda(n, n*pi - S(3)/2 + 17*pi/12), S.Integers)))
    assert solveset_real(tan(x) - tan(pi/10), x).dummy_eq(
        ImageSet(Lambda(n, n*pi + pi/10), S.Integers))
    assert solveset_complex(tan(x) - tan(pi/10), x).dummy_eq(
        ImageSet(Lambda(n, n*pi + pi/10), S.Integers))

    assert solveset_real(3*cosh(2*x) - 5, x) == FiniteSet(
        -acosh(S(5)/3)/2, acosh(S(5)/3)/2)
    assert solveset_complex(3*cosh(2*x) - 5, x).dummy_eq(Union(
        ImageSet(Lambda(n, n*I*pi - acosh(S(5)/3)/2), S.Integers),
        ImageSet(Lambda(n, n*I*pi + acosh(S(5)/3)/2), S.Integers)))
    assert solveset_real(sinh(x - 3) - 2, x) == FiniteSet(
        asinh(2) + 3)
    assert solveset_complex(sinh(x - 3) - 2, x).dummy_eq(Union(
        ImageSet(Lambda(n, 2*n*I*pi + asinh(2) + 3), S.Integers),
        ImageSet(Lambda(n, 2*n*I*pi - asinh(2) + 3 + I*pi), S.Integers)))

    assert solveset_real(cos(sinh(x))-cos(pi/12), x).dummy_eq(Union(
        ImageSet(Lambda(n, asinh(2*n*pi + pi/12)), S.Integers),
        ImageSet(Lambda(n, asinh(2*n*pi + 23*pi/12)), S.Integers)))
    assert solveset(cos(sinh(x))-cos(pi/12), x, Interval(2,3)) == \
        FiniteSet(asinh(23*pi/12), asinh(25*pi/12))
    assert solveset_real(cosh(x**2-1)-2, x) == FiniteSet(
        -sqrt(1 + acosh(2)), sqrt(1 + acosh(2)))

    assert solveset_real(sin(x) - 2, x) == S.EmptySet   # issue #17334
    assert solveset_real(cos(x) + 2, x) == S.EmptySet
    assert solveset_real(sec(x), x) == S.EmptySet
    assert solveset_real(csc(x), x) == S.EmptySet
    assert solveset_real(cosh(x) + 1, x) == S.EmptySet
    assert solveset_real(coth(x), x) == S.EmptySet
    assert solveset_real(sech(x) - 2, x) == S.EmptySet
    assert solveset_real(sech(x), x) == S.EmptySet
    assert solveset_real(tanh(x) + 1, x) == S.EmptySet
    assert solveset_complex(tanh(x), 1) == S.EmptySet
    assert solveset_complex(coth(x), -1) == S.EmptySet
    assert solveset_complex(sech(x), 0) == S.EmptySet
    assert solveset_complex(csch(x), 0) == S.EmptySet

    assert solveset_real(abs(csch(x)) - 3, x) == FiniteSet(-acsch(3), acsch(3))

    assert solveset_real(tanh(x**2 - 1) - exp(-9), x) == FiniteSet(
        -sqrt(atanh(exp(-9)) + 1), sqrt(atanh(exp(-9)) + 1))

    assert solveset_real(coth(log(x)) + 2, x) == FiniteSet(exp(-acoth(2)))
    assert solveset_real(coth(exp(x)) + 2, x) == S.EmptySet

    assert solveset_complex(sinh(x) - I/2, x).dummy_eq(Union(
        ImageSet(Lambda(n, 2*I*pi*n + 5*I*pi/6), S.Integers),
        ImageSet(Lambda(n, 2*I*pi*n + I*pi/6), S.Integers)))
    assert solveset_complex(sinh(x/10) + Rational(3, 4), x).dummy_eq(Union(
        ImageSet(Lambda(n, 20*n*I*pi - 10*asinh(S(3)/4)), S.Integers),
        ImageSet(Lambda(n, 20*n*I*pi + 10*asinh(S(3)/4) + 10*I*pi), S.Integers)))
    assert solveset_complex(sech(sqrt(2)*x/3) + 5, x).dummy_eq(Union(
        ImageSet(Lambda(n, 3*sqrt(2)*(2*n*I*pi - asech(-5))/2), S.Integers),
        ImageSet(Lambda(n, 3*sqrt(2)*(2*n*I*pi + asech(-5))/2), S.Integers)))
    assert solveset_complex(cosh(9*x), x).dummy_eq(Union(
        ImageSet(Lambda(n, 2*n*I*pi/9 + I*pi/18), S.Integers),
        ImageSet(Lambda(n, 2*n*I*pi/9 + I*pi/6), S.Integers)))

    eq = (x**5 -4*x + 1).subs(x, coth(z))
    assert solveset(eq, z, S.Complexes).dummy_eq(Union(
        ImageSet(Lambda(n, n*I*pi + acoth(CRootOf(x**5 -4*x + 1, 0))), S.Integers),
        ImageSet(Lambda(n, n*I*pi + acoth(CRootOf(x**5 -4*x + 1, 1))), S.Integers),
        ImageSet(Lambda(n, n*I*pi + acoth(CRootOf(x**5 -4*x + 1, 2))), S.Integers),
        ImageSet(Lambda(n, n*I*pi + acoth(CRootOf(x**5 -4*x + 1, 3))), S.Integers),
        ImageSet(Lambda(n, n*I*pi + acoth(CRootOf(x**5 -4*x + 1, 4))), S.Integers)))
    assert solveset(eq, z, S.Reals) == FiniteSet(
        acoth(CRootOf(x**5 - 4*x + 1, 0)), acoth(CRootOf(x**5 - 4*x + 1, 2)))

    eq = ((x-sqrt(3)/2)*(x+2)).expand().subs(x, cos(x))
    assert solveset(eq, x, S.Complexes).dummy_eq(Union(
        ImageSet(Lambda(n, 2*n*pi - acos(-2)), S.Integers),
        ImageSet(Lambda(n, 2*n*pi + acos(-2)), S.Integers),
        ImageSet(Lambda(n, 2*n*pi + pi/6), S.Integers),
        ImageSet(Lambda(n, 2*n*pi + 11*pi/6), S.Integers)))
    assert solveset(eq, x, S.Reals).dummy_eq(Union(
        ImageSet(Lambda(n, 2*n*pi + pi/6), S.Integers),
        ImageSet(Lambda(n, 2*n*pi + 11*pi/6), S.Integers)))

    assert solveset((1+sec(sqrt(3)*x+4)**2)/(1-sec(sqrt(3)*x+4))).dummy_eq(Union(
        ImageSet(Lambda(n, sqrt(3)*(2*n*pi - 4 - asec(I))/3), S.Integers),
        ImageSet(Lambda(n, sqrt(3)*(2*n*pi - 4 + asec(I))/3), S.Integers),
        ImageSet(Lambda(n, sqrt(3)*(2*n*pi - 4 - asec(-I))/3), S.Integers),
        ImageSet(Lambda(n, sqrt(3)*(2*n*pi - 4 + asec(-I))/3), S.Integers)))

    assert all_close(solveset(tan(3.14*x)**(S(3)/2)-5.678, x, Interval(0, 3)),
        FiniteSet(0.403301114561067, 0.403301114561067 + 0.318471337579618*pi,
                0.403301114561067 + 0.636942675159236*pi))

