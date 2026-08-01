
def test_issue_6981():
    S = set(divisors(4)).union(set(divisors(Integer(2))))
    assert S == {1,2,4}

