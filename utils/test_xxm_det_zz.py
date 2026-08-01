
def test_XXM_det_ZZ(DM):
    assert DM([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).det() == 0
    assert DM([[1, 2, 3], [4, 5, 6], [7, 8, 10]]).det() == -3

