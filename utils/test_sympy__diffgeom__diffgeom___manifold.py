
def test_sympy__diffgeom__diffgeom__Manifold():
    from sympy.diffgeom import Manifold
    assert _test_args(Manifold('name', 3))

