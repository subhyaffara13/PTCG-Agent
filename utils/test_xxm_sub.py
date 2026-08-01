
def test_XXM_sub(DM):
    A = DM([[1, 2, 3], [4, 5, 6]])
    B = DM([[1, 2, 3], [4, 5, 6]])
    C = DM([[0, 0, 0], [0, 0, 0]])
    assert A.sub(B) == C

