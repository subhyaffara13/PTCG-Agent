
def test_XXM_diagonal(DM):
    assert DM([[1, 0, 0], [0, 5, 0]]).diagonal() == [1, 5]

