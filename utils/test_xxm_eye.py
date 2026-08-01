
def test_XXM_eye(DM):
    T = type(DM([[0]]))
    assert T.eye(3, ZZ) == DM([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert T.eye((3, 2), ZZ) == DM([[1, 0], [0, 1], [0, 0]])

