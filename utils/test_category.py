
def test_category():
    A = Object("A")
    B = Object("B")
    C = Object("C")

    f = NamedMorphism(A, B, "f")
    g = NamedMorphism(B, C, "g")

    d1 = Diagram([f, g])
    d2 = Diagram([f])

    objects = d1.objects | d2.objects

    K = Category("K", objects, commutative_diagrams=[d1, d2])

    assert K.name == "K"
    assert K.objects == Class(objects)
    assert K.commutative_diagrams == FiniteSet(d1, d2)

    raises(ValueError, lambda: Category(""))

