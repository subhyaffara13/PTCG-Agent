
def test_halfcircle_fail():
    r, th = symbols('r, theta', real=True)
    L = Lambda(((r, th),), (r*cos(th), r*sin(th)))
    halfcircle = ImageSet(L, Interval(0, 1)*Interval(0, pi))
    assert (r, 2*pi) not in halfcircle

