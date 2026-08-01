
def test_issue_19766():
    assert limit(2**(-x)*sqrt(4**(x + 1) + 1), x, oo) == 2

