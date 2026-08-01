
def test_XXM_diag(DM):
    T = type(DM([[0]]))
    assert T.diag([1, 2, 3], ZZ) == DM([[1, 0, 0], [0, 2, 0], [0, 0, 3]])

