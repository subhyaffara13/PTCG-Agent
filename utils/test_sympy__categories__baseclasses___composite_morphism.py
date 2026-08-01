
def test_sympy__categories__baseclasses__CompositeMorphism():
    from sympy.categories import Object, NamedMorphism, CompositeMorphism
    A = Object("A")
    B = Object("B")
    C = Object("C")
    f = NamedMorphism(A, B, "f")
    g = NamedMorphism(B, C, "g")
    assert _test_args(CompositeMorphism(f, g))

