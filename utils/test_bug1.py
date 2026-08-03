import re

def test_bug1():
    assert re(x) != x
    x.series(x, 0, 1)
    assert re(x) != x


def test_bug1():
    e = sqrt(-log(w))
    assert e.subs(log(w), -x) == sqrt(x)

    e = sqrt(-5*log(w))
    assert e.subs(log(w), -x) == sqrt(5*x)

