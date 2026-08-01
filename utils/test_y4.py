
def test_Y4():
    t = symbols('t', positive=True)
    s = symbols('s')
    F, _, _ = laplace_transform(erf(3/sqrt(t)), t, s, simplify=True)
    assert F == 1/s - exp(-6*sqrt(s))/s

