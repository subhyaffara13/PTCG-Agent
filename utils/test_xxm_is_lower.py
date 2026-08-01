
def test_XXM_is_lower(DM):
    assert DM([[1, 0, 0], [4, 5, 0]]).is_lower() is True
    assert DM([[1, 2, 3], [4, 5, 6]]).is_lower() is False

