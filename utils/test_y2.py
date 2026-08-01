
def test_Y2():
    t = symbols('t', positive=True)
    w = symbols('w', real=True)
    s = symbols('s')
    f = inverse_laplace_transform(s/(s**2 + (w - 1)**2), s, t, simplify=True)
    assert f == cos(t*(w - 1))

