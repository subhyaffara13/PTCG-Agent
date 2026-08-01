
def test_XXM_from_ddm(DM):
    T = type(DM([[0]]))
    ddm = DDM([[1, 2, 4], [4, 5, 6]], (2, 3), ZZ)
    assert T.from_ddm(ddm) == DM([[1, 2, 4], [4, 5, 6]])

