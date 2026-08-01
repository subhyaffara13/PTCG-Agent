
def test_degree_printing():
    expr1 = 90*degree
    assert pretty(expr1) == '90°'
    expr2 = x*degree
    assert pretty(expr2) == 'x°'
    expr3 = cos(x*degree + 90*degree)
    assert pretty(expr3) == 'cos(x° + 90°)'

