
def test_vector_integrate():
    halfdisc = ParametricRegion((r*cos(theta), r* sin(theta)), (r, -2, 2), (theta, 0, pi))
    assert vector_integrate(C.x**2, halfdisc) == 4*pi
    assert vector_integrate(C.x, ParametricRegion((t, t**2), (t, 2, 3))) == -17*sqrt(17)/12 + 37*sqrt(37)/12

    assert  vector_integrate(C.y**3*C.z, (C.x, 0, 3), (C.y, -1, 4)) == 765*C.z/4

    s1 = Segment(Point(0, 0), Point(0, 1))
    assert vector_integrate(-15*C.y, s1) == S(-15)/2
    s2 = Segment(Point(4, 3, 9), Point(1, 1, 7))
    assert vector_integrate(C.y*C.i, s2) == -6

    curve = Curve((sin(t), cos(t)), (t, 0, 2))
    assert vector_integrate(5*C.z, curve) == 10*C.z

    c1 = Circle(Point(2, 3), 6)
    assert vector_integrate(C.x*C.y, c1) == 72*pi
    c2 = Circle(Point(0, 0), Point(1, 1), Point(1, 0))
    assert vector_integrate(1, c2) == c2.circumference

    triangle = Polygon((0, 0), (1, 0), (1, 1))
    assert vector_integrate(C.x*C.i - 14*C.y*C.j, triangle) == 0
    p1, p2, p3, p4 = [(0, 0), (1, 0), (5, 1), (0, 1)]
    poly = Polygon(p1, p2, p3, p4)
    assert vector_integrate(-23*C.z, poly) == -161*C.z - 23*sqrt(17)*C.z

    point = Point(2, 3)
    assert vector_integrate(C.i*C.y, point) == ParametricIntegral(C.y*C.i, ParametricRegion((2, 3)))

    c3 = ImplicitRegion((x, y), x**2 + y**2 - 4)
    assert vector_integrate(45, c3) == 180*pi
    c4 = ImplicitRegion((x, y), (x - 3)**2 + (y - 4)**2 - 9)
    assert vector_integrate(1, c4) == 6*pi

    pl = Plane(Point(1, 1, 1), Point(2, 3, 4), Point(2, 2, 2))
    raises(ValueError, lambda: vector_integrate(C.x*C.z*C.i + C.k, pl))

