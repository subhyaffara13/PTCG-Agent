
def test_arguments():
    """Functions accepting `Point` objects in `geometry`
    should also accept tuples, lists, and generators and
    automatically convert them to points."""
    from sympy.utilities.iterables import subsets

    singles2d = ((1, 2), [1, 3], Point(1, 5))
    doubles2d = subsets(singles2d, 2)
    l2d = Line(Point2D(1, 2), Point2D(2, 3))
    singles3d = ((1, 2, 3), [1, 2, 4], Point(1, 2, 6))
    doubles3d = subsets(singles3d, 2)
    l3d = Line(Point3D(1, 2, 3), Point3D(1, 1, 2))
    singles4d = ((1, 2, 3, 4), [1, 2, 3, 5], Point(1, 2, 3, 7))
    doubles4d = subsets(singles4d, 2)
    l4d = Line(Point(1, 2, 3, 4), Point(2, 2, 2, 2))
    # test 2D
    test_single = ['contains', 'distance', 'equals', 'parallel_line', 'perpendicular_line', 'perpendicular_segment',
                   'projection', 'intersection']
    for p in doubles2d:
        Line2D(*p)
    for func in test_single:
        for p in singles2d:
            getattr(l2d, func)(p)
    # test 3D
    for p in doubles3d:
        Line3D(*p)
    for func in test_single:
        for p in singles3d:
            getattr(l3d, func)(p)
    # test 4D
    for p in doubles4d:
        Line(*p)
    for func in test_single:
        for p in singles4d:
            getattr(l4d, func)(p)


def test_arguments():
    """Functions accepting `Point` objects in `geometry`
    should also accept tuples and lists and
    automatically convert them to points."""

    singles2d = ((1,2), [1,2], Point(1,2))
    singles2d2 = ((1,3), [1,3], Point(1,3))
    doubles2d = cartes(singles2d, singles2d2)
    p2d = Point2D(1,2)
    singles3d = ((1,2,3), [1,2,3], Point(1,2,3))
    doubles3d = subsets(singles3d, 2)
    p3d = Point3D(1,2,3)
    singles4d = ((1,2,3,4), [1,2,3,4], Point(1,2,3,4))
    doubles4d = subsets(singles4d, 2)
    p4d = Point(1,2,3,4)

    # test 2D
    test_single = ['distance', 'is_scalar_multiple', 'taxicab_distance', 'midpoint', 'intersection', 'dot', 'equals', '__add__', '__sub__']
    test_double = ['is_concyclic', 'is_collinear']
    for p in singles2d:
        Point2D(p)
    for func in test_single:
        for p in singles2d:
            getattr(p2d, func)(p)
    for func in test_double:
        for p in doubles2d:
            getattr(p2d, func)(*p)

    # test 3D
    test_double = ['is_collinear']
    for p in singles3d:
        Point3D(p)
    for func in test_single:
        for p in singles3d:
            getattr(p3d, func)(p)
    for func in test_double:
        for p in doubles3d:
            getattr(p3d, func)(*p)

    # test 4D
    test_double = ['is_collinear']
    for p in singles4d:
        Point(p)
    for func in test_single:
        for p in singles4d:
            getattr(p4d, func)(p)
    for func in test_double:
        for p in doubles4d:
            getattr(p4d, func)(*p)

    # test evaluate=False for ops
    x = Symbol('x')
    a = Point(0, 1)
    assert a + (0.1, x) == Point(0.1, 1 + x, evaluate=False)
    a = Point(0, 1)
    assert a/10.0 == Point(0, 0.1, evaluate=False)
    a = Point(0, 1)
    assert a*10.0 == Point(0, 10.0, evaluate=False)

    # test evaluate=False when changing dimensions
    u = Point(.1, .2, evaluate=False)
    u4 = Point(u, dim=4, on_morph='ignore')
    assert u4.args == (.1, .2, 0, 0)
    assert all(i.is_Float for i in u4.args[:2])
    # and even when *not* changing dimensions
    assert all(i.is_Float for i in Point(u).args)

    # never raise error if creating an origin
    assert Point(dim=3, on_morph='error')

    # raise error with unmatched dimension
    raises(ValueError, lambda: Point(1, 1, dim=3, on_morph='error'))
    # test unknown on_morph
    raises(ValueError, lambda: Point(1, 1, dim=3, on_morph='unknown'))
    # test invalid expressions
    raises(TypeError, lambda: Point(Basic(), Basic()))

