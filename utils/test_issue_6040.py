
def test_issue_6040():
    a, b = Pow(1, 2, evaluate=False), S.One
    assert a != b
    assert b != a
    assert not (a == b)
    assert not (b == a)

