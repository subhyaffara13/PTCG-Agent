
def test_XXM_from_list(DM):
    T = type(DM([[0]]))

    lol = [[1, 2, 4], [4, 5, 6]]
    lol_ZZ = [[ZZ(1), ZZ(2), ZZ(4)], [ZZ(4), ZZ(5), ZZ(6)]]
    lol_ZZ_bad = [[ZZ(1), ZZ(2), ZZ(4)], [ZZ(4), ZZ(5), ZZ(6), ZZ(7)]]

    assert T.from_list(lol_ZZ, (2, 3), ZZ) == DM(lol)
    raises(DMBadInputError, lambda: T.from_list(lol_ZZ_bad, (3, 2), ZZ))

