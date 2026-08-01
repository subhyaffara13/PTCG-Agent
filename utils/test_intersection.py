
def test_intersection():
    # iterable
    i = Intersection(FiniteSet(1, 2, 3), Interval(2, 5), evaluate=False)
    assert i.is_iterable
    assert set(i) == {S(2), S(3)}

    # challenging intervals
    x = Symbol('x', real=True)
    i = Intersection(Interval(0, 3), Interval(x, 6))
    assert (5 in i) is False
    raises(TypeError, lambda: 2 in i)

    # Singleton special cases
    assert Intersection(Interval(0, 1), S.EmptySet) == S.EmptySet
    assert Intersection(Interval(-oo, oo), Interval(-oo, x)) == Interval(-oo, x)

    # Products
    line = Interval(0, 5)
    i = Intersection(line**2, line**3, evaluate=False)
    assert (2, 2) not in i
    assert (2, 2, 2) not in i
    raises(TypeError, lambda: list(i))

    a = Intersection(Intersection(S.Integers, S.Naturals, evaluate=False), S.Reals, evaluate=False)
    assert a._argset == frozenset([Intersection(S.Naturals, S.Integers, evaluate=False), S.Reals])

    assert Intersection(S.Complexes, FiniteSet(S.ComplexInfinity)) == S.EmptySet

    # issue 12178
    assert Intersection() == S.UniversalSet

    # issue 16987
    assert Intersection({1}, {1}, {x}) == Intersection({1}, {x})


def test_intersection():
    R = QQ.old_poly_ring(x, y, z)
    # SCA, example 1.8.11
    assert R.ideal(x, y).intersect(R.ideal(y**2, z)) == R.ideal(y**2, y*z, x*z)

    assert R.ideal(x, y).intersect(R.ideal()).is_zero()

    R = QQ.old_poly_ring(x, y, z, order="ilex")
    assert R.ideal(x, y).intersect(R.ideal(y**2 + y**2*z, z + z*x**3*y)) == \
        R.ideal(y**2, y*z, x*z)


def test_intersection():
    # SCA, example 2.8.5
    F = QQ.old_poly_ring(x, y).free_module(2)
    M1 = F.submodule([x, y], [y, 1])
    M2 = F.submodule([0, y - 1], [x, 1], [y, x])
    I = F.submodule([x, y], [y**2 - y, y - 1], [x*y + y, x + 1])
    I1, rel1, rel2 = M1.intersect(M2, relations=True)
    assert I1 == M2.intersect(M1) == I
    for i, g in enumerate(I1.gens):
        assert g == sum(c*x for c, x in zip(rel1[i], M1.gens)) \
                 == sum(d*y for d, y in zip(rel2[i], M2.gens))

    assert F.submodule([x, y]).intersect(F.submodule([y, x])).is_zero()


def test_intersection():
    poly1 = Triangle(Point(0, 0), Point(1, 0), Point(0, 1))
    poly2 = Polygon(Point(0, 1), Point(-5, 0),
                    Point(0, -4), Point(0, Rational(1, 5)),
                    Point(S.Half, -0.1), Point(1, 0), Point(0, 1))

    assert poly1.intersection(poly2) == [Point2D(Rational(1, 3), 0),
        Segment(Point(0, Rational(1, 5)), Point(0, 0)),
        Segment(Point(1, 0), Point(0, 1))]
    assert poly2.intersection(poly1) == [Point(Rational(1, 3), 0),
        Segment(Point(0, 0), Point(0, Rational(1, 5))),
        Segment(Point(1, 0), Point(0, 1))]
    assert poly1.intersection(Point(0, 0)) == [Point(0, 0)]
    assert poly1.intersection(Point(-12,  -43)) == []
    assert poly2.intersection(Line((-12, 0), (12, 0))) == [Point(-5, 0),
        Point(0, 0), Point(Rational(1, 3), 0), Point(1, 0)]
    assert poly2.intersection(Line((-12, 12), (12, 12))) == []
    assert poly2.intersection(Ray((-3, 4), (1, 0))) == [Segment(Point(1, 0),
        Point(0, 1))]
    assert poly2.intersection(Circle((0, -1), 1)) == [Point(0, -2),
        Point(0, 0)]
    assert poly1.intersection(poly1) == [Segment(Point(0, 0), Point(1, 0)),
        Segment(Point(0, 1), Point(0, 0)), Segment(Point(1, 0), Point(0, 1))]
    assert poly2.intersection(poly2) == [Segment(Point(-5, 0), Point(0, -4)),
        Segment(Point(0, -4), Point(0, Rational(1, 5))),
        Segment(Point(0, Rational(1, 5)), Point(S.Half, Rational(-1, 10))),
        Segment(Point(0, 1), Point(-5, 0)),
        Segment(Point(S.Half, Rational(-1, 10)), Point(1, 0)),
        Segment(Point(1, 0), Point(0, 1))]
    assert poly2.intersection(Triangle(Point(0, 1), Point(1, 0), Point(-1, 1))) \
        == [Point(Rational(-5, 7), Rational(6, 7)), Segment(Point2D(0, 1), Point(1, 0))]
    assert poly1.intersection(RegularPolygon((-12, -15), 3, 3)) == []


def test_intersection():
    assert intersection(Point(0, 0)) == []
    raises(TypeError, lambda: intersection(Point(0, 0), 3))
    assert intersection(
            Segment((0, 0), (2, 0)),
            Segment((-1, 0), (1, 0)),
            Line((0, 0), (0, 1)), pairwise=True) == [
        Point(0, 0), Segment((0, 0), (1, 0))]
    assert intersection(
            Line((0, 0), (0, 1)),
            Segment((0, 0), (2, 0)),
            Segment((-1, 0), (1, 0)), pairwise=True) == [
        Point(0, 0), Segment((0, 0), (1, 0))]
    assert intersection(
            Line((0, 0), (0, 1)),
            Segment((0, 0), (2, 0)),
            Segment((-1, 0), (1, 0)),
            Line((0, 0), slope=1), pairwise=True) == [
        Point(0, 0), Segment((0, 0), (1, 0))]
    R = 4.0
    c = intersection(
            Ray(Point2D(0.001, -1),
            Point2D(0.0008, -1.7)),
            Ellipse(center=Point2D(0, 0), hradius=R, vradius=2.0), pairwise=True)[0].coordinates
    assert c == pytest.approx(
            Point2D(0.000714285723396502, -1.99999996811224, evaluate=False).coordinates)
    # check this is responds to a lower precision parameter
    R = Float(4, 5)
    c2 = intersection(
            Ray(Point2D(0.001, -1),
            Point2D(0.0008, -1.7)),
            Ellipse(center=Point2D(0, 0), hradius=R, vradius=2.0), pairwise=True)[0].coordinates
    assert c2 == pytest.approx(
            Point2D(0.000714285723396502, -1.99999996811224, evaluate=False).coordinates)
    assert c[0]._prec == 53
    assert c2[0]._prec == 20


def test_intersection(idx, sort):
    piece1 = idx[:5][::-1]
    piece2 = idx[3:]

    the_int = piece1.intersection(piece2, sort=sort)

    if sort in (None, True):
        tm.assert_index_equal(the_int, idx[3:5])
    else:
        tm.assert_index_equal(the_int.sort_values(), idx[3:5])

    # corner case, pass self
    the_int = idx.intersection(idx, sort=sort)
    tm.assert_index_equal(the_int, idx)

    # empty intersection: disjoint
    empty = idx[:2].intersection(idx[2:], sort=sort)
    expected = idx[:0]
    assert empty.equals(expected)

    tuples = idx.values
    result = idx.intersection(tuples)
    assert result.equals(idx)


def test_intersection():
    G = nx.Graph()
    H = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4])
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    H.add_nodes_from([1, 2, 3, 4])
    H.add_edge(2, 3)
    H.add_edge(3, 4)
    I = nx.intersection(G, H)
    assert set(I.nodes()) == {1, 2, 3, 4}
    assert sorted(I.edges()) == [(2, 3)]

