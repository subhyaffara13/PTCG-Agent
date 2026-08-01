
def test_sympy__diffgeom__diffgeom__CovarDerivativeOp():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, BaseVectorField, CovarDerivativeOp
    cs = CoordSystem('name', Patch('name', Manifold('name', 3)), [a, b, c])
    v = BaseVectorField(cs, 0)
    _test_args(CovarDerivativeOp(v, [[[0, ]*3, ]*3, ]*3))

