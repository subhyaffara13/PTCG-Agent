
def test_issue_2877():
    f = Float(2.0)
    assert (x + f).subs({f: 2}) == x + 2

    def r(a, b, c):
        return factor(a*x**2 + b*x + c)
    e = r(5.0/6, 10, 5)
    assert nsimplify(e) == 5*x**2/6 + 10*x + 5

