
def test_issue_18041():
    e = -sqrt(-2 + 2*sqrt(3)*I)
    assert sqrtdenest(e) == -1 - sqrt(3)*I

