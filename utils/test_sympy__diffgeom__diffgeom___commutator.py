
def test_sympy__diffgeom__diffgeom__Commutator():
    from sympy.diffgeom import Manifold, Patch, CoordSystem, BaseVectorField, Commutator
    cs = CoordSystem('name', Patch('name', Manifold('name', 3)), [a, b, c])
    cs1 = CoordSystem('name1', Patch('name', Manifold('name', 3)), [a, b, c])
    v = BaseVectorField(cs, 0)
    v1 = BaseVectorField(cs1, 0)
    assert _test_args(Commutator(v, v1))

