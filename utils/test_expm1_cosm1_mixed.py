
def test_expm1_cosm1_mixed():
    x = Symbol('x')
    expr1 = exp(x) + cos(x) - 2
    opt1 = optimize(expr1, [expm1_opt, cosm1_opt])
    assert opt1 == cosm1(x) + expm1(x)

