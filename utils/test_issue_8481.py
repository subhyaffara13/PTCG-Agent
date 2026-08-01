
def test_issue_8481():
    k = Symbol('k', integer=True, nonnegative=True)
    lamda = Symbol('lamda', positive=True)
    assert limit(lamda**k * exp(-lamda) / factorial(k), k, oo) == 0

