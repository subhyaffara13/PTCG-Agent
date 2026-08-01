
def test_XXM_charpoly_ZZ(DM):
    dM1 = DM([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
    assert dM1.charpoly() == [1, -16, -12, 3]

