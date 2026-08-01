
def test_solve_polynomial_cv_1a():
    """
    Test for solving on equations that can be converted to a polynomial equation
    using the change of variable y -> x**Rational(p, q)
    """
    assert solve( sqrt(x) - 1, x) == [1]
    assert solve( sqrt(x) - 2, x) == [4]
    assert solve( x**Rational(1, 4) - 2, x) == [16]
    assert solve( x**Rational(1, 3) - 3, x) == [27]
    assert solve(sqrt(x) + x**Rational(1, 3) + x**Rational(1, 4), x) == [0]


def test_solve_polynomial_cv_1a():
    """
    Test for solving on equations that can be converted to
    a polynomial equation using the change of variable y -> x**Rational(p, q)
    """
    assert solveset_real(sqrt(x) - 1, x) == FiniteSet(1)
    assert solveset_real(sqrt(x) - 2, x) == FiniteSet(4)
    assert solveset_real(x**Rational(1, 4) - 2, x) == FiniteSet(16)
    assert solveset_real(x**Rational(1, 3) - 3, x) == FiniteSet(27)
    assert solveset_real(x*(x**(S.One / 3) - 3), x) == \
        FiniteSet(S.Zero, S(27))

