
def test_logaddexp2_opt():
    x, y = map(Symbol, 'x y'.split())
    expr1 = log(2**x + 2**y)/log(2)
    opt1 = optimize(expr1, [logaddexp2_opt])
    assert logaddexp2(x, y) - opt1 == 0
    assert logaddexp2(y, x) - opt1 == 0
    assert opt1.rewrite(log) == expr1

