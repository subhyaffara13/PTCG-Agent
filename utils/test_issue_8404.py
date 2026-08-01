
def test_issue_8404():
    i = Symbol('i', integer=True)
    assert Abs(Sum(1/(3*i + 1)**2, (i, 0, S.Infinity)).doit().n(4)
        - 1.122) < 0.001

