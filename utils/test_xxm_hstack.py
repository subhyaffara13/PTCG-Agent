
def test_XXM_hstack(DM):
    A = DM([[1, 2, 3], [4, 5, 6]])
    B = DM([[7, 8], [9, 10]])
    C = DM([[1, 2, 3, 7, 8], [4, 5, 6, 9, 10]])
    ABC = DM([[1, 2, 3, 7, 8, 1, 2, 3, 7, 8],
              [4, 5, 6, 9, 10, 4, 5, 6, 9, 10]])
    assert A.hstack(B) == C
    assert A.hstack(B, C) == ABC

