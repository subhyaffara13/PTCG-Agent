
def test_sympy__diffgeom__diffgeom__BaseScalarField():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, BaseScalarField
    cs = CoordSystem('name', Patch('name', Manifold('name', 3)), [a, b, c])
    assert _test_args(BaseScalarField(cs, 0))

