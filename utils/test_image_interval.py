
def test_image_interval():
    x = Symbol('x', real=True)
    a = Symbol('a', real=True)
    assert imageset(x, 2*x, Interval(-2, 1)) == Interval(-4, 2)
    assert imageset(x, 2*x, Interval(-2, 1, True, False)) == \
        Interval(-4, 2, True, False)
    assert imageset(x, x**2, Interval(-2, 1, True, False)) == \
        Interval(0, 4, False, True)
    assert imageset(x, x**2, Interval(-2, 1)) == Interval(0, 4)
    assert imageset(x, x**2, Interval(-2, 1, True, False)) == \
        Interval(0, 4, False, True)
    assert imageset(x, x**2, Interval(-2, 1, True, True)) == \
        Interval(0, 4, False, True)
    assert imageset(x, (x - 2)**2, Interval(1, 3)) == Interval(0, 1)
    assert imageset(x, 3*x**4 - 26*x**3 + 78*x**2 - 90*x, Interval(0, 4)) == \
        Interval(-35, 0)  # Multiple Maxima
    assert imageset(x, x + 1/x, Interval(-oo, oo)) == Interval(-oo, -2) \
        + Interval(2, oo)  # Single Infinite discontinuity
    assert imageset(x, 1/x + 1/(x-1)**2, Interval(0, 2, True, False)) == \
        Interval(Rational(3, 2), oo, False)  # Multiple Infinite discontinuities

    # Test for Python lambda
    assert imageset(lambda x: 2*x, Interval(-2, 1)) == Interval(-4, 2)

    assert imageset(Lambda(x, a*x), Interval(0, 1)) == \
            ImageSet(Lambda(x, a*x), Interval(0, 1))

    assert imageset(Lambda(x, sin(cos(x))), Interval(0, 1)) == \
            ImageSet(Lambda(x, sin(cos(x))), Interval(0, 1))

