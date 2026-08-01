
def test_sympy__diffgeom__diffgeom__BaseCovarDerivativeOp():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, BaseCovarDerivativeOp
    cs = CoordSystem('name', Patch('name', Manifold('name', 3)), [a, b, c])
    assert _test_args(BaseCovarDerivativeOp(cs, 0, [[[0, ]*3, ]*3, ]*3))

