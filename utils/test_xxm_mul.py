
def test_XXM_mul(DM):
    A = DM([[1, 2, 3], [4, 5, 6]])
    b = ZZ(2)
    assert A.mul(b) == DM([[2, 4, 6], [8, 10, 12]])
    assert A.rmul(b) == DM([[2, 4, 6], [8, 10, 12]])

