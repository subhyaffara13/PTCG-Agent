
def test_image_Intersection():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    assert imageset(x, x**2, Interval(-2, 0).intersect(Interval(x, y))) == \
           Interval(0, 4).intersect(Interval(Min(x**2, y**2), Max(x**2, y**2)))

