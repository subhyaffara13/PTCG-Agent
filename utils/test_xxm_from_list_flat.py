
def test_XXM_from_list_flat(DM):
    T = type(DM([[0]]))
    flat = [ZZ(1), ZZ(2), ZZ(4), ZZ(4), ZZ(5), ZZ(6)]
    assert T.from_list_flat(flat, (2, 3), ZZ) == DM([[1, 2, 4], [4, 5, 6]])
    raises(DMBadInputError, lambda: T.from_list_flat(flat, (3, 3), ZZ))

