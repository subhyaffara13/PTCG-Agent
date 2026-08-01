
def test_cosm1_two_cos_terms():
    x, y = map(Symbol, 'x y'.split())
    expr1 = cos(x) + cos(y) - 2
    opt1 = optimize(expr1, [cosm1_opt])
    assert opt1 == cosm1(x) + cosm1(y)

