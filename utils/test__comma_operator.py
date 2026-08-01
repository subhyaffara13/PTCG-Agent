
def test_CommaOperator():
    expr = CommaOperator(PreIncrement(x), 2*x)
    assert ccode(expr) == '(++(x), 2*x)'
    assert expr.func(*expr.args) == expr

