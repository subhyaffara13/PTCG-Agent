
def test_issue_19558():
    e = (7*x*cos(x) - 12*log(x)**3)*(-log(x)**4 + 2*sin(x) + 1)**2/ \
    (2*(x*cos(x) - 2*log(x)**3)*(3*log(x)**4 - 7*sin(x) + 3)**2)

    assert e.subs(x, oo) == AccumBounds(-oo, oo)
    assert (sin(x) + cos(x)).subs(x, oo) == AccumBounds(-2, 2)

