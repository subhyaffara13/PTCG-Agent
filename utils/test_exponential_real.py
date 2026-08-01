
def test_exponential_real():
    from sympy.abc import y

    e1 = 3**(2*x) - 2**(x + 3)
    e2 = 4**(5 - 9*x) - 8**(2 - x)
    e3 = 2**x + 4**x
    e4 = exp(log(5)*x) - 2**x
    e5 = exp(x/y)*exp(-z/y) - 2
    e6 = 5**(x/2) - 2**(x/3)
    e7 = 4**(x + 1) + 4**(x + 2) + 4**(x - 1) - 3**(x + 2) - 3**(x + 3)
    e8 = -9*exp(-2*x + 5) + 4*exp(3*x + 1)
    e9 = 2**x + 4**x + 8**x - 84
    e10 = 29*2**(x + 1)*615**(x) - 123*2726**(x)

    assert solveset(e1, x, S.Reals) == FiniteSet(
        -3*log(2)/(-2*log(3) + log(2)))
    assert solveset(e2, x, S.Reals) == FiniteSet(Rational(4, 15))
    assert solveset(e3, x, S.Reals) == S.EmptySet
    assert solveset(e4, x, S.Reals) == FiniteSet(0)
    assert solveset(e5, x, S.Reals) == Intersection(
        S.Reals, FiniteSet(y*log(2*exp(z/y))))
    assert solveset(e6, x, S.Reals) == FiniteSet(0)
    assert solveset(e7, x, S.Reals) == FiniteSet(2)
    assert solveset(e8, x, S.Reals) == FiniteSet(-2*log(2)/5 + 2*log(3)/5 + Rational(4, 5))
    assert solveset(e9, x, S.Reals) == FiniteSet(2)
    assert solveset(e10,x, S.Reals) == FiniteSet((-log(29) - log(2) + log(123))/(-log(2726) + log(2) + log(615)))

    assert solveset_real(-9*exp(-2*x + 5) + 2**(x + 1), x) == FiniteSet(
        -((-5 - 2*log(3) + log(2))/(log(2) + 2)))
    assert solveset_real(4**(x/2) - 2**(x/3), x) == FiniteSet(0)
    b = sqrt(6)*sqrt(log(2))/sqrt(log(5))
    assert solveset_real(5**(x/2) - 2**(3/x), x) == FiniteSet(-b, b)

    # coverage test
    C1, C2 = symbols('C1 C2')
    f = Function('f')
    assert solveset_real(C1 + C2/x**2 - exp(-f(x)), f(x)) == Intersection(
        S.Reals, FiniteSet(-log(C1 + C2/x**2)))
    y = symbols('y', positive=True)
    assert solveset_real(x**2 - y**2/exp(x), y) == Intersection(
        S.Reals, FiniteSet(-sqrt(x**2*exp(x)), sqrt(x**2*exp(x))))
    p = Symbol('p', positive=True)
    assert solveset_real((1/p + 1)**(p + 1), p).dummy_eq(
        ConditionSet(x, Eq((1 + 1/x)**(x + 1), 0), S.Reals))
    assert solveset(2**x - 4**x + 12, x, S.Reals) == {2}
    assert solveset(2**x - 2**(2*x) + 12, x, S.Reals) == {2}

