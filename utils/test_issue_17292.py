
def test_issue_17292():
    assert simplify(abs(x)/abs(x**2)) == 1/abs(x)
    # this is bigger than the issue: check that deep processing works
    assert simplify(5*abs((x**2 - 1)/(x - 1))) == 5*Abs(x + 1)

