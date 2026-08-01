
def test_math():
    f = lambdify((x, y), sin(x), modules="math")
    assert f(0, 5) == 0

