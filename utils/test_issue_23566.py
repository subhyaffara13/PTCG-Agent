import math


def test_issue_23566():
    i = integrate(1/sqrt(x**2-1), (x, -2, -1))
    assert i == -log(2 - sqrt(3))
    assert math.isclose(i.n(), 1.31695789692482)


def test_issue_23566():
    i = Integral(1/sqrt(x**2 - 1), (x, -2, -1)).doit(manual=True)
    assert i == -log(4 - 2*sqrt(3)) + log(2)
    assert str(i.n()) == '1.31695789692482'

