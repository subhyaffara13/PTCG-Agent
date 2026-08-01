
def test_XXM_is_upper(DM):
    assert DM([[1, 2, 3], [0, 5, 6]]).is_upper() is True
    assert DM([[1, 2, 3], [4, 5, 6]]).is_upper() is False
    assert DM([]).is_upper() is True
    assert DM([[], []]).is_upper() is True

