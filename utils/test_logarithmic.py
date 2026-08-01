
def test_logarithmic():
    assert solveset_real(log(x - 3) + log(x + 3), x) == FiniteSet(
        -sqrt(10), sqrt(10))
    assert solveset_real(log(x + 1) - log(2*x - 1), x) == FiniteSet(2)
    assert solveset_real(log(x + 3) + log(1 + 3/x) - 3, x) == FiniteSet(
        -3 + sqrt(-12 + exp(3))*exp(Rational(3, 2))/2 + exp(3)/2,
        -sqrt(-12 + exp(3))*exp(Rational(3, 2))/2 - 3 + exp(3)/2)

    eq = z - log(x) + log(y/(x*(-1 + y**2/x**2)))
    assert solveset_real(eq, x) == \
        Intersection(S.Reals, FiniteSet(-sqrt(y**2 - y*exp(z)),
            sqrt(y**2 - y*exp(z)))) - \
        Intersection(S.Reals, FiniteSet(-sqrt(y**2), sqrt(y**2)))
    assert solveset_real(
        log(3*x) - log(-x + 1) - log(4*x + 1), x) == FiniteSet(Rational(-1, 2), S.Half)
    assert solveset(log(x**y) - y*log(x), x, S.Reals) == S.Reals

