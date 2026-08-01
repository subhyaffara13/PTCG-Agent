
def test_XXM_applyfunc(DM):
    A = DM([[1, 2, 3], [4, 5, 6]])
    B = DM([[2, 4, 6], [8, 10, 12]])
    assert A.applyfunc(lambda x: 2*x, ZZ) == B

