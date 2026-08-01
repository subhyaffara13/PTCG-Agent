
def test_XXM_ones(DM):
    T = type(DM([[0]]))
    assert T.ones((2, 3), ZZ) == DM([[1, 1, 1], [1, 1, 1]])

