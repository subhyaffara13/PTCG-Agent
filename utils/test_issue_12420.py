
def test_issue_12420():
    assert sqrtdenest((3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2) == I
    e = 3 - sqrt(2)*sqrt(4 + I) + 3*I
    assert sqrtdenest(e) == e

