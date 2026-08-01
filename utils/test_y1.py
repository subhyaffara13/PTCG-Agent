
def test_Y1():
    t = symbols('t', positive=True)
    w = symbols('w', real=True)
    s = symbols('s')
    F, _, _ = laplace_transform(cos((w - 1)*t), t, s)
    assert F == s/(s**2 + (w - 1)**2)

