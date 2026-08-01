
def test_issue_27380():
    assert simplify(1.0**(x+1)/1.0**x) == 1.0

