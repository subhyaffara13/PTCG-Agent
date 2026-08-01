
def test_sympy__diffgeom__diffgeom__CoordinateSymbol():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, CoordinateSymbol
    assert _test_args(CoordinateSymbol(CoordSystem('name', Patch('name', Manifold('name', 3)), [a, b, c]), 0))

