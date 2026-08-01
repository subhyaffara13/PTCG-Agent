
def test_issue_14196():
    k, n  = symbols('k, n', positive=True)
    m = Symbol('m')
    assert limit_seq(Sum(m**k, (m, 1, n)).doit()/(n**(k + 1)), n) == 1/(k + 1)

