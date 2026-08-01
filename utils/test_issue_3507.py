
def test_issue_3507():
    e = x**(-4)*(x**2 - x**2*sqrt(cos(x)))
    assert e.nseries(x, n=9) == \
        Rational(1, 4) + x**2/96 + 19*x**4/5760 + 559*x**6/645120 + 29161*x**8/116121600 + O(x**9)

