
def test_max_degree():
    polygon = Polygon((0, 0), (0, 1), (1, 1), (1, 0))
    polys = [1, x, y, x*y, x**2*y, x*y**2]
    assert polytope_integrate(polygon, polys, max_degree=3) == \
        {1: 1, x: S.Half, y: S.Half, x*y: Rational(1, 4), x**2*y: Rational(1, 6), x*y**2: Rational(1, 6)}
    assert polytope_integrate(polygon, polys, max_degree=2) == \
        {1: 1, x: S.Half, y: S.Half, x*y: Rational(1, 4)}
    assert polytope_integrate(polygon, polys, max_degree=1) == \
        {1: 1, x: S.Half, y: S.Half}

