
def test_integrate_linearterm_pow():
    # check integrate((a*x+b)^c, x)  --  issue 3499
    y = Symbol('y', positive=True)
    # TODO: Remove conds='none' below, let the assumption take care of it.
    assert integrate(x**y, x, conds='none') == x**(y + 1)/(y + 1)
    assert integrate((exp(y)*x + 1/y)**(1 + sin(y)), x, conds='none') == \
        exp(-y)*(exp(y)*x + 1/y)**(2 + sin(y)) / (2 + sin(y))

