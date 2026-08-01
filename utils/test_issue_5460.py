
def test_issue_5460():
    u = Mul(2, (1 + x), evaluate=False)
    assert (2 + u).args == (2, u)

