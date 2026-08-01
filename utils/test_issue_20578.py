
def test_issue_20578():
    expr = abs(x) * sin(1/x)
    assert limit(expr,x,0,'+') == 0
    assert limit(expr,x,0,'-') == 0
    assert limit(expr,x,0,'+-') == 0

