
def test_issue_4516():
    assert integrate(2**x - 2*x, x) == 2**x/log(2) - x**2

