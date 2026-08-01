
def test_sympy__categories__baseclasses__NamedMorphism():
    from sympy.categories import Object, NamedMorphism
    assert _test_args(NamedMorphism(Object("A"), Object("B"), "f"))

