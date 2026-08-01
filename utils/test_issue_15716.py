
def test_issue_15716():
    e = Integral(factorial(x), (x, -oo, oo))
    assert e.as_terms() == ([(e, ((1.0, 0.0), (1,), ()))], [e])

