
def test_issue_25582():

    assert limit(asin(exp(x)), x, oo, '-') == -oo*I
    assert limit(acos(exp(x)), x, oo, '-') == oo*I
    assert limit(atan(exp(x)), x, oo, '-') == pi/2
    assert limit(acot(exp(x)), x, oo, '-') == 0
    assert limit(asec(exp(x)), x, oo, '-') == pi/2
    assert limit(acsc(exp(x)), x, oo, '-') == 0

