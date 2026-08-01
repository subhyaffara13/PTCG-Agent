
def test_issue_5673():
    eq = -x + exp(exp(LambertW(log(x)))*LambertW(log(x)))
    assert checksol(eq, x, 2) is True
    assert checksol(eq, x, 2, numerical=False) is None


def test_issue_5673():
    e = LambertW(-1)
    assert e.is_comparable is False
    assert e.is_positive is not True
    e2 = 1 - 1/(1 - exp(-1000))
    assert e2.is_positive is not True
    e3 = -2 + exp(exp(LambertW(log(2)))*LambertW(log(2)))
    assert e3.is_nonzero is not True

