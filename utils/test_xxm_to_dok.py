
def test_XXM_to_dok(DM):
    dod = {(0, 0): ZZ(1), (0, 2): ZZ(4),
           (1, 0): ZZ(4), (1, 1): ZZ(5), (1, 2): ZZ(6)}
    assert DM([[1, 0, 4], [4, 5, 6]]).to_dok() == dod

