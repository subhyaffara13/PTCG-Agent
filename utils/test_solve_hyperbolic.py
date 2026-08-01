
def test_solve_hyperbolic():
    # actual solver: _solve_trig1
    n = Dummy('n')
    assert solveset(sinh(x) + cosh(x), x) == S.EmptySet
    assert solveset(sinh(x) + cos(x), x) == ConditionSet(x,
        Eq(cos(x) + sinh(x), 0), S.Complexes)
    assert solveset_real(sinh(x) + sech(x), x) == FiniteSet(
        log(sqrt(sqrt(5) - 2)))
    assert solveset_real(cosh(2*x) + 2*sinh(x) - 5, x) == FiniteSet(
        log(-2 + sqrt(5)), log(1 + sqrt(2)))
    assert solveset_real((coth(x) + sinh(2*x))/cosh(x) - 3, x) == FiniteSet(
        log(S.Half + sqrt(5)/2), log(1 + sqrt(2)))
    assert solveset_real(cosh(x)*sinh(x) - 2, x) == FiniteSet(
        log(4 + sqrt(17))/2)
    assert solveset_real(sinh(x) + tanh(x) - 1, x) == FiniteSet(
        log(sqrt(2)/2 + sqrt(-S(1)/2 + sqrt(2))))

    assert dumeq(solveset_complex(sinh(x) + sech(x), x), Union(
        ImageSet(Lambda(n, 2*n*I*pi + log(sqrt(-2 + sqrt(5)))), S.Integers),
        ImageSet(Lambda(n, I*(2*n*pi + pi/2) + log(sqrt(2 + sqrt(5)))), S.Integers),
        ImageSet(Lambda(n, I*(2*n*pi + pi) + log(sqrt(-2 + sqrt(5)))), S.Integers),
        ImageSet(Lambda(n, I*(2*n*pi - pi/2) + log(sqrt(2 + sqrt(5)))), S.Integers)))

    assert dumeq(solveset(cosh(x/15) + cosh(x/5)), Union(
        ImageSet(Lambda(n, 15*I*(2*n*pi + pi/2)), S.Integers),
        ImageSet(Lambda(n, 15*I*(2*n*pi - pi/2)), S.Integers),
        ImageSet(Lambda(n, 15*I*(2*n*pi - 3*pi/4)), S.Integers),
        ImageSet(Lambda(n, 15*I*(2*n*pi + 3*pi/4)), S.Integers),
        ImageSet(Lambda(n, 15*I*(2*n*pi - pi/4)), S.Integers),
        ImageSet(Lambda(n, 15*I*(2*n*pi + pi/4)), S.Integers)))

    assert dumeq(solveset(tanh(pi*x) - coth(pi/2*x)), Union(
        ImageSet(Lambda(n, 2*I*(2*n*pi + pi/2)/pi), S.Integers),
        ImageSet(Lambda(n, 2*I*(2*n*pi - pi/2)/pi), S.Integers)))

    # issues #18490 / #19489
    assert solveset(cosh(x) + cosh(3*x) - cosh(5*x), x, S.Reals
        ).dummy_eq(ConditionSet(x,
        Eq(cosh(x) + cosh(3*x) - cosh(5*x), 0), S.Reals))
    assert solveset(sinh(8*x) + coth(12*x)).dummy_eq(
        ConditionSet(x, Eq(sinh(8*x) + coth(12*x), 0), S.Complexes))

