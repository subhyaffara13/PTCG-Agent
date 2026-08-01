
def test_XXM_qr_non_field(DM):
    lol = [[ZZ(3), ZZ(1)], [ZZ(4), ZZ(3)]]
    A = DM(lol)
    with pytest.raises(DMDomainError):
        A.qr()

