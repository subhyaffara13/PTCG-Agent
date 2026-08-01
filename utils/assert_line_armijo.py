
def assert_line_armijo(x, p, s, f, **kw):
    assert_armijo(s, phi=lambda sp: f(x + p*sp), **kw)

