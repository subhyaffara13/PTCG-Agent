
def test_XXM_matmul(DM):
    A = DM([[1, 2, 3], [4, 5, 6]])
    B = DM([[1, 2], [3, 4], [5, 6]])
    C = DM([[22, 28], [49, 64]])
    assert A.matmul(B) == C

