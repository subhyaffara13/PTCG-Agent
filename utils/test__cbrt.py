
def test_Cbrt():
    x = Symbol('x')

    # Expand
    assert Cbrt(x).expand(func=True) - x**Rational(1, 3) == 0

    # Diff
    assert Cbrt(42*x).diff(x) - 42*(42*x)**(Rational(1, 3) - 1)/3 == 0
    assert Cbrt(42*x).diff(x) - Cbrt(42*x).expand(func=True).diff(x) == 0

