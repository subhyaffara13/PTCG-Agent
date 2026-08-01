
def test_simplify_rational():
    expr = 2**x*2.**y
    assert simplify(expr, rational = True) == 2**(x+y)
    assert simplify(expr, rational = None) == 2.0**(x+y)
    assert simplify(expr, rational = False) == expr
    assert simplify('0.9 - 0.8 - 0.1', rational = True) == 0

