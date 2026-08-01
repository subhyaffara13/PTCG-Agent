
def test_point():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    x1 = Symbol('x1', real=True)
    x2 = Symbol('x2', real=True)
    y1 = Symbol('y1', real=True)
    y2 = Symbol('y2', real=True)
    half = S.Half
    p1 = Point(x1, x2)
    p2 = Point(y1, y2)
    p3 = Point(0, 0)
    p4 = Point(1, 1)
    p5 = Point(0, 1)
    line = Line(Point(1, 0), slope=1)

    assert p1 in p1
    assert p1 not in p2
    assert p2.y == y2
    assert (p3 + p4) == p4
    assert (p2 - p1) == Point(y1 - x1, y2 - x2)
    assert -p2 == Point(-y1, -y2)
    raises(TypeError, lambda: Point(1))
    raises(ValueError, lambda: Point([1]))
    raises(ValueError, lambda: Point(3, I))
    raises(ValueError, lambda: Point(2*I, I))
    raises(ValueError, lambda: Point(3 + I, I))

    assert Point(34.05, sqrt(3)) == Point(Rational(681, 20), sqrt(3))
    assert Point.midpoint(p3, p4) == Point(half, half)
    assert Point.midpoint(p1, p4) == Point(half + half*x1, half + half*x2)
    assert Point.midpoint(p2, p2) == p2
    assert p2.midpoint(p2) == p2
    assert p1.origin == Point(0, 0)

    assert Point.distance(p3, p4) == sqrt(2)
    assert Point.distance(p1, p1) == 0
    assert Point.distance(p3, p2) == sqrt(p2.x**2 + p2.y**2)
    raises(TypeError, lambda: Point.distance(p1, 0))
    raises(TypeError, lambda: Point.distance(p1, GeometryEntity()))

    # distance should be symmetric
    assert p1.distance(line) == line.distance(p1)
    assert p4.distance(line) == line.distance(p4)

    assert Point.taxicab_distance(p4, p3) == 2

    assert Point.canberra_distance(p4, p5) == 1
    raises(ValueError, lambda: Point.canberra_distance(p3, p3))

    p1_1 = Point(x1, x1)
    p1_2 = Point(y2, y2)
    p1_3 = Point(x1 + 1, x1)
    assert Point.is_collinear(p3)

    with warns(UserWarning, test_stacklevel=False):
        assert Point.is_collinear(p3, Point(p3, dim=4))
    assert p3.is_collinear()
    assert Point.is_collinear(p3, p4)
    assert Point.is_collinear(p3, p4, p1_1, p1_2)
    assert Point.is_collinear(p3, p4, p1_1, p1_3) is False
    assert Point.is_collinear(p3, p3, p4, p5) is False

    raises(TypeError, lambda: Point.is_collinear(line))
    raises(TypeError, lambda: p1_1.is_collinear(line))

    assert p3.intersection(Point(0, 0)) == [p3]
    assert p3.intersection(p4) == []
    assert p3.intersection(line) == []
    with warns(UserWarning, test_stacklevel=False):
        assert Point.intersection(Point(0, 0, 0), Point(0, 0)) == [Point(0, 0, 0)]

    x_pos = Symbol('x', positive=True)
    p2_1 = Point(x_pos, 0)
    p2_2 = Point(0, x_pos)
    p2_3 = Point(-x_pos, 0)
    p2_4 = Point(0, -x_pos)
    p2_5 = Point(x_pos, 5)
    assert Point.is_concyclic(p2_1)
    assert Point.is_concyclic(p2_1, p2_2)
    assert Point.is_concyclic(p2_1, p2_2, p2_3, p2_4)
    for pts in permutations((p2_1, p2_2, p2_3, p2_5)):
        assert Point.is_concyclic(*pts) is False
    assert Point.is_concyclic(p4, p4 * 2, p4 * 3) is False
    assert Point(0, 0).is_concyclic((1, 1), (2, 2), (2, 1)) is False
    assert Point.is_concyclic(Point(0, 0, 0, 0), Point(1, 0, 0, 0), Point(1, 1, 0, 0), Point(1, 1, 1, 0)) is False

    assert p1.is_scalar_multiple(p1)
    assert p1.is_scalar_multiple(2*p1)
    assert not p1.is_scalar_multiple(p2)
    assert Point.is_scalar_multiple(Point(1, 1), (-1, -1))
    assert Point.is_scalar_multiple(Point(0, 0), (0, -1))
    # test when is_scalar_multiple can't be determined
    raises(Undecidable, lambda: Point.is_scalar_multiple(Point(sympify("x1%y1"), sympify("x2%y2")), Point(0, 1)))

    assert Point(0, 1).orthogonal_direction == Point(1, 0)
    assert Point(1, 0).orthogonal_direction == Point(0, 1)

    assert p1.is_zero is None
    assert p3.is_zero
    assert p4.is_zero is False
    assert p1.is_nonzero is None
    assert p3.is_nonzero is False
    assert p4.is_nonzero

    assert p4.scale(2, 3) == Point(2, 3)
    assert p3.scale(2, 3) == p3

    assert p4.rotate(pi, Point(0.5, 0.5)) == p3
    assert p1.__radd__(p2) == p1.midpoint(p2).scale(2, 2)
    assert (-p3).__rsub__(p4) == p3.midpoint(p4).scale(2, 2)

    assert p4 * 5 == Point(5, 5)
    assert p4 / 5 == Point(0.2, 0.2)
    assert 5 * p4 == Point(5, 5)

    raises(ValueError, lambda: Point(0, 0) + 10)

    # Point differences should be simplified
    assert Point(x*(x - 1), y) - Point(x**2 - x, y + 1) == Point(0, -1)

    a, b = S.Half, Rational(1, 3)
    assert Point(a, b).evalf(2) == \
        Point(a.n(2), b.n(2), evaluate=False)
    raises(ValueError, lambda: Point(1, 2) + 1)

    # test project
    assert Point.project((0, 1), (1, 0)) == Point(0, 0)
    assert Point.project((1, 1), (1, 0)) == Point(1, 0)
    raises(ValueError, lambda: Point.project(p1, Point(0, 0)))

    # test transformations
    p = Point(1, 0)
    assert p.rotate(pi/2) == Point(0, 1)
    assert p.rotate(pi/2, p) == p
    p = Point(1, 1)
    assert p.scale(2, 3) == Point(2, 3)
    assert p.translate(1, 2) == Point(2, 3)
    assert p.translate(1) == Point(2, 1)
    assert p.translate(y=1) == Point(1, 2)
    assert p.translate(*p.args) == Point(2, 2)

    # Check invalid input for transform
    raises(ValueError, lambda: p3.transform(p3))
    raises(ValueError, lambda: p.transform(Matrix([[1, 0], [0, 1]])))

    # test __contains__
    assert 0 in Point(0, 0, 0, 0)
    assert 1 not in Point(0, 0, 0, 0)

    # test affine_rank
    assert Point.affine_rank() == -1


def test_point():
    point = Point(cs, [x, y])
    assert point != Point(cs, [2, y])


def test_point():
    x, y = symbols('x, y')
    p = R2_r.point([x, y])
    assert p.free_symbols == {x, y}
    assert p.coords(R2_r) == p.coords() == Matrix([x, y])
    assert p.coords(R2_p) == Matrix([sqrt(x**2 + y**2), atan2(y, x)])

