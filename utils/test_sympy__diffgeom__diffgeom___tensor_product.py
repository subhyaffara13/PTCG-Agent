
def test_sympy__diffgeom__diffgeom__TensorProduct():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, BaseScalarField, Differential, TensorProduct
    cs = CoordSystem('name', Patch('name', Manifold('name', 3)), [a, b, c])
    d = Differential(BaseScalarField(cs, 0))
    assert _test_args(TensorProduct(d, d))

