
def test_comparison():
    assert Ordinal(OmegaPower(5, 3)) > Ordinal(OmegaPower(4, 3), OmegaPower(2, 1))
    assert Ordinal(OmegaPower(5, 3), OmegaPower(3, 2)) < Ordinal(OmegaPower(5, 4))
    assert Ordinal(OmegaPower(5, 4)) < Ordinal(OmegaPower(5, 5), OmegaPower(4, 1))

    assert Ordinal(OmegaPower(5, 3), OmegaPower(3, 2)) == \
        Ordinal(OmegaPower(5, 3), OmegaPower(3, 2))
    assert not Ordinal(OmegaPower(5, 3), OmegaPower(3, 2)) == Ordinal(OmegaPower(5, 3))
    assert Ordinal(OmegaPower(omega, 3)) > Ordinal(OmegaPower(5, 3))

