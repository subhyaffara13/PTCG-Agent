
def test_sympy__categories__baseclasses__Diagram():
    from sympy.categories import Object, NamedMorphism, Diagram
    A = Object("A")
    B = Object("B")
    f = NamedMorphism(A, B, "f")
    d = Diagram([f])
    assert _test_args(d)

