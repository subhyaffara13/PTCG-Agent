
def test_XXM_vstack(DM):
    A = DM([[1, 2, 3], [4, 5, 6]])
    B = DM([[7, 8, 9]])
    C = DM([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    ABC = DM([[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert A.vstack(B) == C
    assert A.vstack(B, C) == ABC

