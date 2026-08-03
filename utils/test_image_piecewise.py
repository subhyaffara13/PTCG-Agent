from typing import Union

def test_image_piecewise():
    f = Piecewise((x, x <= -1), (1/x**2, x <= 5), (x**3, True))
    f1 = Piecewise((0, x <= 1), (1, x <= 2), (2, True))
    assert imageset(x, f, Interval(-5, 5)) == Union(Interval(-5, -1), Interval(Rational(1, 25), oo))
    assert imageset(x, f1, Interval(1, 2)) == FiniteSet(0, 1)

