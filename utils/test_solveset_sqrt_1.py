
def test_solveset_sqrt_1():
    assert solveset_real(sqrt(5*x + 6) - 2 - x, x) == \
        FiniteSet(-S.One, S(2))
    assert solveset_real(sqrt(x - 1) - x + 7, x) == FiniteSet(10)
    assert solveset_real(sqrt(x - 2) - 5, x) == FiniteSet(27)
    assert solveset_real(sqrt(x) - 2 - 5, x) == FiniteSet(49)
    assert solveset_real(sqrt(x**3), x) == FiniteSet(0)
    assert solveset_real(sqrt(x - 1), x) == FiniteSet(1)
    assert solveset_real(sqrt((x-3)/x), x) == FiniteSet(3)
    assert solveset_real(sqrt((x-3)/x)-Rational(1, 2), x) == \
        FiniteSet(4)

