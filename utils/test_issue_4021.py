
def test_issue_4021():
    e = Integral(x, x) + 1
    assert str(e) == 'Integral(x, x) + 1'

