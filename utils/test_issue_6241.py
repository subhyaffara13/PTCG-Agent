
def test_issue_6241():
    z = sqrt( -320 + 32*sqrt(5) + 64*r15)
    assert sqrtdenest(z) == z

