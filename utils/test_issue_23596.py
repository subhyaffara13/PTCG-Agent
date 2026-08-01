
def test_issue_23596():
    assert integrate(((1 + x)/x**2)*exp(-1/x), (x, 0, oo)) == oo

