
def test_expr():
    x = symbols('x')
    raises(TypeError, lambda: tan(x).series(x, 2, oo, "+"))

