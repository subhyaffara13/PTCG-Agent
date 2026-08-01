
def test_replace_exceptions():
    from sympy.core.symbol import Wild
    x, y = symbols('x y')
    e = (x**2 + x*y)
    raises(TypeError, lambda: e.replace(sin, 2))
    b = Wild('b')
    c = Wild('c')
    raises(TypeError, lambda: e.replace(b*c, c.is_real))
    raises(TypeError, lambda: e.replace(b.is_real, 1))
    raises(TypeError, lambda: e.replace(lambda d: d.is_Number, 1))

