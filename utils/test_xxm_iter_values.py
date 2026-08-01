
def test_XXM_iter_values(DM):
    values = [ZZ(1), ZZ(4), ZZ(4), ZZ(5), ZZ(6)]
    assert sorted(DM([[1, 0, 4], [4, 5, 6]]).iter_values()) == values

