
def test_XXM_to_list_flat(DM):
    lol = [[1, 2, 4], [4, 5, 6]]
    assert DM(lol).to_list_flat() == [ZZ(1), ZZ(2), ZZ(4), ZZ(4), ZZ(5), ZZ(6)]

