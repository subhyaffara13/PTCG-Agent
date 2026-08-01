
def test_morphisms():
    A = Object("A")
    B = Object("B")
    C = Object("C")
    D = Object("D")

    # Test the base morphism.
    f = NamedMorphism(A, B, "f")
    assert f.domain == A
    assert f.codomain == B
    assert f == NamedMorphism(A, B, "f")

    # Test identities.
    id_A = IdentityMorphism(A)
    id_B = IdentityMorphism(B)
    assert id_A.domain == A
    assert id_A.codomain == A
    assert id_A == IdentityMorphism(A)
    assert id_A != id_B

    # Test named morphisms.
    g = NamedMorphism(B, C, "g")
    assert g.name == "g"
    assert g != f
    assert g == NamedMorphism(B, C, "g")
    assert g != NamedMorphism(B, C, "f")

    # Test composite morphisms.
    assert f == CompositeMorphism(f)

    k = g.compose(f)
    assert k.domain == A
    assert k.codomain == C
    assert k.components == Tuple(f, g)
    assert g * f == k
    assert CompositeMorphism(f, g) == k

    assert CompositeMorphism(g * f) == g * f

    # Test the associativity of composition.
    h = NamedMorphism(C, D, "h")

    p = h * g
    u = h * g * f

    assert h * k == u
    assert p * f == u
    assert CompositeMorphism(f, g, h) == u

    # Test flattening.
    u2 = u.flatten("u")
    assert isinstance(u2, NamedMorphism)
    assert u2.name == "u"
    assert u2.domain == A
    assert u2.codomain == D

    # Test identities.
    assert f * id_A == f
    assert id_B * f == f
    assert id_A * id_A == id_A
    assert CompositeMorphism(id_A) == id_A

    # Test bad compositions.
    raises(ValueError, lambda: f * g)

    raises(TypeError, lambda: f.compose(None))
    raises(TypeError, lambda: id_A.compose(None))
    raises(TypeError, lambda: f * None)
    raises(TypeError, lambda: id_A * None)

    raises(TypeError, lambda: CompositeMorphism(f, None, 1))

    raises(ValueError, lambda: NamedMorphism(A, B, ""))
    raises(NotImplementedError, lambda: Morphism(A, B))

