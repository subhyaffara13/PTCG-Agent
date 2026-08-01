
def test_sympy__diffgeom__diffgeom__CoordSystem():
    from sympy.diffgeom import Manifold, Patch, CoordSystem
    assert _test_args(CoordSystem('name', Patch('name', Manifold('name', 3))))
    assert _test_args(CoordSystem('name', Patch('name', Manifold('name', 3)), [a, b, c]))

