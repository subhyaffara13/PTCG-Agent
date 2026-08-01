
def test_XXM_convert_to(DM):
    A = DM([[1, 2, 3], [4, 5, 6]], ZZ)
    B = DM([[1, 2, 3], [4, 5, 6]], QQ)
    assert A.convert_to(QQ) == B
    assert B.convert_to(ZZ) == A

