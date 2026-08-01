
def test_XXM_transpose(DM):
    A = DM([[1, 2, 3], [4, 5, 6]])
    assert A.transpose() == DM([[1, 4], [2, 5], [3, 6]])

