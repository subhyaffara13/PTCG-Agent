
def test_AlgebraicField_galois_group():
    k = QQ.alg_field_from_poly(Poly(x**4 + 1))
    G, _ = k.galois_group(by_name=True)
    assert G == S4TransitiveSubgroups.V

    k = QQ.alg_field_from_poly(Poly(x**4 - 2))
    G, _ = k.galois_group(by_name=True)
    assert G == S4TransitiveSubgroups.D4

