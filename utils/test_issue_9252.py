
def test_issue_9252():
    n = Symbol('n', integer=True)
    c = Symbol('c', positive=True)
    assert limit((log(n))**(n/log(n)) / (1 + c)**n, n, oo) == 0
    # limit should depend on the value of c
    raises(NotImplementedError, lambda: limit((log(n))**(n/log(n)) / c**n, n, oo))

