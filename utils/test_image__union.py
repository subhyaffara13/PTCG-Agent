
def test_image_Union():
    x = Symbol('x', real=True)
    assert imageset(x, x**2, Interval(-2, 0) + FiniteSet(1, 2, 3)) == \
            (Interval(0, 4) + FiniteSet(9))

