
def test_sympy__categories__baseclasses__IdentityMorphism():
    from sympy.categories import Object, IdentityMorphism
    assert _test_args(IdentityMorphism(Object("A")))

