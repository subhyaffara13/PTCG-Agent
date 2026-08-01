
def test_sympy__diffgeom__diffgeom__Point():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, Point
    assert _test_args(Point(
        CoordSystem('name', Patch('name', Manifold('name', 3)), [a, b, c]), [x, y]))

