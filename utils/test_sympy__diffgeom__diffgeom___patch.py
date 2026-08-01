
def test_sympy__diffgeom__diffgeom__Patch():
    from sympy.diffgeom import Manifold, Patch
    assert _test_args(Patch('name', Manifold('name', 3)))

