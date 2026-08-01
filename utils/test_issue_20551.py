
def test_issue_20551():
    expr = (exp(x)/x).series(x, n=None)
    terms = [ next(expr) for i in range(3) ]
    assert terms == [1/x, 1, x/2]

