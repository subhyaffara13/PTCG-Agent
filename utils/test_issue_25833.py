
def test_issue_25833():
    assert limit(atan(x**2), x, oo) == pi/2
    assert limit(atan(x**2 - 1), x, oo) == pi/2
    assert limit(atan(log(2**x)/log(2*x)), x, oo) == pi/2

