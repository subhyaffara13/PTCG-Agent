
def test_XXM_zeros(DM):
    T = type(DM([[0]]))
    assert T.zeros((2, 3), ZZ) == DM([[0, 0, 0], [0, 0, 0]])

