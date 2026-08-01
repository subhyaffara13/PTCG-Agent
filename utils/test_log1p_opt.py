
def test_log1p_opt():
    x = Symbol('x')
    expr1 = log(x + 1)
    opt1 = optimize(expr1, [log1p_opt])
    assert log1p(x) - opt1 == 0
    assert opt1.rewrite(log) == expr1

    expr2 = log(3*x + 3)
    opt2 = optimize(expr2, [log1p_opt])
    assert log1p(x) + log(3) == opt2
    assert (opt2.rewrite(log) - expr2).simplify() == 0

    expr3 = log(2*x + 1)
    opt3 = optimize(expr3, [log1p_opt])
    assert log1p(2*x) - opt3 == 0
    assert opt3.rewrite(log) == expr3

    expr4 = log(x+3)
    opt4 = optimize(expr4, [log1p_opt])
    assert str(opt4) == 'log(x + 3)'

