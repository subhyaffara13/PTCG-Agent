
def test_XXM_neg(DM):
    A = DM([[1, 2, 3], [4, 5, 6]])
    C = DM([[-1, -2, -3], [-4, -5, -6]])
    assert A.neg() == C

