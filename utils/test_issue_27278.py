
def test_issue_27278():
    expr = (1/(x*log((x + 3)/x)))**x*((x + 1)*log((x + 4)/(x + 1)))**(x + 1)/3
    assert limit(expr, x, oo) == 1

