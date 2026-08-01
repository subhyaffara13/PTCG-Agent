
def test_XXM_from_dok(DM):
    T = type(DM([[0]]))
    dod = {(0, 0): ZZ(1), (0, 2): ZZ(4),
           (1, 0): ZZ(4), (1, 1): ZZ(5), (1, 2): ZZ(6)}
    assert T.from_dok(dod, (2, 3), ZZ) == DM([[1, 0, 4], [4, 5, 6]])

