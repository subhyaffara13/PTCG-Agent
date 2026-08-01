
def test_XXM_to_flat_nz(DM):
    M = DM([[1, 2, 0], [0, 0, 0], [0, 0, 3]])
    elements = [ZZ(1), ZZ(2), ZZ(3)]
    indices = ((0, 0), (0, 1), (2, 2))
    assert M.to_flat_nz() == (elements, (indices, M.shape))

