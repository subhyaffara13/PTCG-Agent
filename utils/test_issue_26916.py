
def test_issue_26916():
    assert limit(Ei(x)*exp(-x), x, +oo) == 0
    assert limit(Ei(x)*exp(-x), x, -oo) == 0

