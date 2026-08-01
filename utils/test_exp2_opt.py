
def test_exp2_opt():
    x = Symbol('x')
    expr1 = 1 + 2**x
    opt1 = optimize(expr1, [exp2_opt])
    assert opt1 == 1 + exp2(x)
    assert opt1.rewrite(Pow) == expr1

    expr2 = 1 + 3**x
    assert expr2 == optimize(expr2, [exp2_opt])

