
def test_issue_3502():
    e = sin(5*x)/sin(2*x)
    assert e.nseries(x, n=2) == Rational(5, 2) + O(x**2)
    assert e.nseries(x, n=6) == \
        Rational(5, 2) - 35*x**2/4 + 329*x**4/48 + O(x**6)

