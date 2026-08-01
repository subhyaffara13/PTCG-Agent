
def test_sympy__diffgeom__diffgeom__LieDerivative():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, BaseScalarField, Differential, BaseVectorField, LieDerivative
    cs = CoordSystem('name', Patch('name', Manifold('name', 3)), [a, b, c])
    d = Differential(BaseScalarField(cs, 0))
    v = BaseVectorField(cs, 0)
    assert _test_args(LieDerivative(v, d))

