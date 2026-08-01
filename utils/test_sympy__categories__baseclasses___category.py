
def test_sympy__categories__baseclasses__Category():
    from sympy.categories import Object, NamedMorphism, Diagram, Category
    A = Object("A")
    B = Object("B")
    C = Object("C")
    f = NamedMorphism(A, B, "f")
    g = NamedMorphism(B, C, "g")
    d1 = Diagram([f, g])
    d2 = Diagram([f])
    K = Category("K", commutative_diagrams=[d1, d2])
    assert _test_args(K)

