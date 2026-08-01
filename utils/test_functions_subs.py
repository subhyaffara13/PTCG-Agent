
def test_functions_subs():
    f, g = symbols('f g', cls=Function)
    l = Lambda((x, y), sin(x) + y)
    assert (g(y, x) + cos(x)).subs(g, l) == sin(y) + x + cos(x)
    assert (f(x)**2).subs(f, sin) == sin(x)**2
    assert (f(x, y)).subs(f, log) == log(x, y)
    assert (f(x, y)).subs(f, sin) == f(x, y)
    assert (sin(x) + atan2(x, y)).subs([[atan2, f], [sin, g]]) == \
        f(x, y) + g(x)
    assert (g(f(x + y, x))).subs([[f, l], [g, exp]]) == exp(x + sin(x + y))

