
def test_XXM_is_diagonal(DM):
    assert DM([[1, 0, 0], [0, 5, 0]]).is_diagonal() is True
    assert DM([[1, 2, 3], [4, 5, 6]]).is_diagonal() is False

