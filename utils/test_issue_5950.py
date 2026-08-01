
def test_issue_5950():
    x, y = symbols("x,y", positive=True)
    assert logcombine(log(3) - log(2)) == log(Rational(3,2), evaluate=False)
    assert logcombine(log(x) - log(y)) == log(x/y)
    assert logcombine(log(Rational(3,2), evaluate=False) - log(2)) == \
        log(Rational(3,4), evaluate=False)

