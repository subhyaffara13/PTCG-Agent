
def test_sympy__diffgeom__diffgeom__BaseVectorField():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, BaseVectorField
    cs = CoordSystem('name', Patch('name', Manifold('name', 3)), [a, b, c])
    assert _test_args(BaseVectorField(cs, 0))

