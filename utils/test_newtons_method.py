
def test_newtons_method():
    x, dx, atol = symbols('x dx atol')
    expr = cos(x) - x**3
    algo = newtons_method(expr, x, atol, dx)
    assert algo.has(Assignment(dx, -expr/expr.diff(x)))

