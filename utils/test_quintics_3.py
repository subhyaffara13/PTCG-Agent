
def test_quintics_3():
    y = x**5 + x**3 - 2**Rational(1, 3)
    assert solve(y) == solve(-y) == []

