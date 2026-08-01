
def test_integer_powers():
    assert integer_powers([x, x/2, x**2 + 1, x*Rational(2, 3)]) == [
            (x/6, [(x, 6), (x/2, 3), (x*Rational(2, 3), 4)]),
            (1 + x**2, [(1 + x**2, 1)])]

