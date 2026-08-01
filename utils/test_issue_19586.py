
def test_issue_19586():
    assert limit(x**(2**x*3**(-x)), x, oo) == 1

