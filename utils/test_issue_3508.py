
def test_issue_3508():
    x = Symbol("x", real=True)
    assert log(sin(x)).series(x, n=5) == log(x) - x**2/6 - x**4/180 + O(x**5)
    e = -log(x) + x*(-log(x) + log(sin(2*x))) + log(sin(2*x))
    assert e.series(x, n=5) == \
        log(2) + log(2)*x - 2*x**2/3 - 2*x**3/3 - 4*x**4/45 + O(x**5)

