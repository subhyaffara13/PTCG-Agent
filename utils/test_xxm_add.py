
def test_XXM_add(DM):
    A = DM([[1, 2, 3], [4, 5, 6]])
    B = DM([[1, 2, 3], [4, 5, 6]])
    C = DM([[2, 4, 6], [8, 10, 12]])
    assert A.add(B) == C

