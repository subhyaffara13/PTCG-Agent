
def test_halfcircle():
    r, th = symbols('r, theta', real=True)
    L = Lambda(((r, th),), (r*cos(th), r*sin(th)))
    halfcircle = ImageSet(L, Interval(0, 1)*Interval(0, pi))

    assert (1, 0) in halfcircle
    assert (0, -1) not in halfcircle
    assert (0, 0) in halfcircle
    assert halfcircle._contains((r, 0)) is None
    assert not halfcircle.is_iterable

