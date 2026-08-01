
def test_issue_8866():
    assert simplify(log(x, 10, evaluate=False)) == simplify(log(x, 10))
    assert expand_log(log(x, 10, evaluate=False)) == expand_log(log(x, 10))

    y = Symbol('y', positive=True)
    l1 = log(exp(y), exp(10))
    b1 = log(exp(y), exp(5))
    l2 = log(exp(y), exp(10), evaluate=False)
    b2 = log(exp(y), exp(5), evaluate=False)
    assert simplify(log(l1, b1)) == simplify(log(l2, b2))
    assert expand_log(log(l1, b1)) == expand_log(log(l2, b2))

