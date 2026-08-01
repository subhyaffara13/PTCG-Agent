
def test_other_lambert():
    assert solve(3*sin(x) - x*sin(3), x) == [3]
    assert set(solve(x**a - a**x), x) == {
        a, -a*LambertW(-log(a)/a)/log(a)}


def test_other_lambert():
    a = Rational(6, 5)
    assert solveset_real(x**a - a**x, x) == FiniteSet(
        a, -a*LambertW(-log(a)/a)/log(a))

