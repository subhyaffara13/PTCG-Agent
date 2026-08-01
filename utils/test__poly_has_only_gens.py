
def test_Poly_has_only_gens():
    assert Poly(x*y + 1, x, y, z).has_only_gens(x, y) is True
    assert Poly(x*y + z, x, y, z).has_only_gens(x, y) is False

    raises(GeneratorsError, lambda: Poly(x*y**2 + y**2, x, y).has_only_gens(t))

