
def test_logaddexp_opt():
    x, y = map(Symbol, 'x y'.split())
    expr1 = log(exp(x) + exp(y))
    opt1 = optimize(expr1, [logaddexp_opt])
    assert logaddexp(x, y) - opt1 == 0
    assert logaddexp(y, x) - opt1 == 0
    assert opt1.rewrite(log) == expr1

