
def test_XXM_iter_items(DM):
    items = [((0, 0), ZZ(1)), ((0, 2), ZZ(4)),
             ((1, 0), ZZ(4)), ((1, 1), ZZ(5)), ((1, 2), ZZ(6))]
    assert sorted(DM([[1, 0, 4], [4, 5, 6]]).iter_items()) == items

