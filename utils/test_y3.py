
def test_Y3():
    t = symbols('t', positive=True)
    w = symbols('w', real=True)
    s = symbols('s')
    F, _, _ = laplace_transform(sinh(w*t)*cosh(w*t), t, s, simplify=True)
    assert F == w/(s**2 - 4*w**2)

