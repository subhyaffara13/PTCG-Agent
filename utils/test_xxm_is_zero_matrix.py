
def test_XXM_is_zero_matrix(DM):
    assert DM([[0, 0, 0], [0, 0, 0]]).is_zero_matrix() is True
    assert DM([[1, 0, 0], [0, 0, 0]]).is_zero_matrix() is False

