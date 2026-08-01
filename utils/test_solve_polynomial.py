
def test_solve_polynomial():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    assert solveset_real(3*x - 2, x) == FiniteSet(Rational(2, 3))

    assert solveset_real(x**2 - 1, x) == FiniteSet(-S.One, S.One)
    assert solveset_real(x - y**3, x) == FiniteSet(y ** 3)

    assert solveset_real(x**3 - 15*x - 4, x) == FiniteSet(
        -2 + 3 ** S.Half,
        S(4),
        -2 - 3 ** S.Half)

    assert solveset_real(sqrt(x) - 1, x) == FiniteSet(1)
    assert solveset_real(sqrt(x) - 2, x) == FiniteSet(4)
    assert solveset_real(x**Rational(1, 4) - 2, x) == FiniteSet(16)
    assert solveset_real(x**Rational(1, 3) - 3, x) == FiniteSet(27)
    assert len(solveset_real(x**5 + x**3 + 1, x)) == 1
    assert len(solveset_real(-2*x**3 + 4*x**2 - 2*x + 6, x)) > 0
    assert solveset_real(x**6 + x**4 + I, x) is S.EmptySet

