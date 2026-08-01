
def test_sympy__diffgeom__diffgeom__Differential():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, BaseScalarField, Differential
    cs = CoordSystem('name', Patch('name', Manifold('name', 3)), [a, b, c])
    assert _test_args(Differential(BaseScalarField(cs, 0)))

