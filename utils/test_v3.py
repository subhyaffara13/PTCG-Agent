
def test_V3():
    assert integrate(1/(x**3 + 2),x).diff().simplify() == 1/(x**3 + 2)

