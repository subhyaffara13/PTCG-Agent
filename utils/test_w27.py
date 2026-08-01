
def test_W27():
    a, b, c = symbols('a b c')
    assert integrate(integrate(integrate(1, (z, 0, c*(1 - x/a - y/b))),
                               (y, 0, b*(1 - x/a))),
                     (x, 0, a)) == a*b*c/6

