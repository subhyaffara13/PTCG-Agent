
def test_J17():
    assert integrate(f((x + 2)/5)*DiracDelta((x - 2)/3) - g(x)*diff(DiracDelta(x - 1), x), (x, 0, 3)) == 3*f(R(4, 5)) + Subs(Derivative(g(x), x), x, 1)

