
def test_addition_with_integers():
    assert 3 + Ordinal(OmegaPower(5, 3)) == Ordinal(OmegaPower(5, 3))
    assert Ordinal(OmegaPower(5, 3))+3 == Ordinal(OmegaPower(5, 3), OmegaPower(0, 3))
    assert Ordinal(OmegaPower(5, 3), OmegaPower(0, 2))+3 == \
        Ordinal(OmegaPower(5, 3), OmegaPower(0, 5))

