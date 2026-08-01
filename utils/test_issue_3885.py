
def test_issue_3885():
    assert limit(x*y + x*z, z, 2) == x*y + 2*x

