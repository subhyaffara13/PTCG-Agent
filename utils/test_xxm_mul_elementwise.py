
def test_XXM_mul_elementwise(DM):
    A = DM([[1, 2, 3], [4, 5, 6]])
    B = DM([[1, 2, 3], [4, 5, 6]])
    C = DM([[1, 4, 9], [16, 25, 36]])
    assert A.mul_elementwise(B) == C

